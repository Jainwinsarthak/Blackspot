"""Generate deterministic, geographically plausible Delhi road and crash demo data."""
from __future__ import annotations
from pathlib import Path
import json
import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
ROAD_CONFIG = {
    "highway": (0.10, (4, 6), (60, 100), (12, 20), .80),
    "arterial": (0.25, (3, 5), (45, 70), (9, 16), .60),
    "collector": (0.30, (2, 4), (30, 55), (7, 12), .35),
    "residential": (0.35, (1, 2), (20, 40), (4, 8), .10),
}
NAMES = {"highway": ["NH-48", "Outer Ring Road", "Delhi–Meerut Expressway"], "arterial": ["Ring Road", "Aurobindo Marg", "Mehrauli Road"], "collector": ["Vikas Marg", "Najafgarh Road", "Mathura Road"], "residential": ["Sector Link Road", "Colony Road", "Market Lane"]}

def choice_bool(p: np.ndarray | float) -> np.ndarray: return RNG.random(len(p) if isinstance(p, np.ndarray) else 1) < p

def create_segments(n: int = 3500) -> pd.DataFrame:
    road_types = RNG.choice(list(ROAD_CONFIG), n, p=[ROAD_CONFIG[x][0] for x in ROAD_CONFIG])
    rows = []
    for i, rt in enumerate(road_types, 1):
        _, lanes, speeds, widths, median_p = ROAD_CONFIG[rt]
        lat, lon = RNG.uniform(28.40, 28.88), RNG.uniform(76.84, 77.35)
        angle, distance = RNG.uniform(0, 2*np.pi), RNG.uniform(.001, .008)
        complex_j = int(RNG.choice([2, 3, 4, 5, 6], p=[.26, .30, .24, .14, .06]))
        commercial = float(np.clip(RNG.beta(4, 3) if rt == "arterial" else RNG.beta(2, 5), 0, 1))
        rows.append({
            "segment_id": i, "osm_way_id": 800000+i, "name": f"{RNG.choice(NAMES[rt])} {i/10:.1f}",
            "lat_start": lat, "lon_start": lon, "lat_end": lat+distance*np.sin(angle), "lon_end": lon+distance*np.cos(angle),
            "road_type": rt, "lane_count": int(RNG.integers(lanes[0],lanes[1]+1)), "speed_limit_kmh": int(RNG.integers(speeds[0], speeds[1]+1)),
            "surface": "unpaved" if RNG.random() < (.08 if rt == "residential" else .01) else "paved", "has_median": int(RNG.random()<median_p),
            "has_signal": int(RNG.random() < .12+.12*complex_j), "has_streetlight": int(RNG.random() < (.84 if rt != "residential" else .58)),
            "has_pedestrian_crossing": int(RNG.random() < (.52 if rt == "residential" else .26)), "has_speed_breaker": int(RNG.random() < (.42 if rt == "residential" else .12)),
            "road_curvature_radius_m": round(float(RNG.uniform(45, 700 if rt == "highway" else 450)), 1), "elevation_change_m": round(float(RNG.gamma(2, 1.8)),1),
            "sight_distance_m": round(float(RNG.uniform(30, 250)),1), "junction_type": RNG.choice(["none","T","cross","roundabout"], p=[.30,.31,.31,.08]), "junction_complexity": complex_j,
            "school_within_200m": int(RNG.random() < (.35 if rt == "residential" else .12)), "hospital_within_500m": int(RNG.random()<.10), "bus_stop_within_100m": int(RNG.random() < (.52 if rt in ["arterial","collector"] else .20)),
            "commercial_density": round(commercial,3), "population_density": round(float(RNG.beta(2.5,2)),3), "avg_rainfall_mm": round(float(RNG.uniform(18, 95)),1), "fog_days_per_year": int(RNG.integers(5, 32)), "road_width_m": round(float(RNG.uniform(widths[0], widths[1])),1)
        })
    return pd.DataFrame(rows)

def risk_propensity(s: pd.DataFrame) -> np.ndarray:
    return (1.5*(1-s.has_median)+1.3*(1-s.has_streetlight)+1.1*(1-s.has_signal)+1.0*(s.road_curvature_radius_m<120)+.75*(s.speed_limit_kmh>60)+.6*s.junction_complexity+.65*s.school_within_200m+.45*s.commercial_density).to_numpy()

def create_accidents(segments: pd.DataFrame, n: int = 2800) -> pd.DataFrame:
    p = np.exp(risk_propensity(segments)/2.5); p /= p.sum()
    sampled = segments.iloc[RNG.choice(len(segments), n, p=p)].reset_index(drop=True)
    dates = pd.to_datetime(RNG.integers(pd.Timestamp("2020-01-01").value//10**9, pd.Timestamp("2026-01-01").value//10**9, n), unit="s")
    hour_weights = np.array([2,1,1,1,1,2,3,5,8,8,7,5,5,5,6,8,9,10,10,7,5,4,3,2], dtype=float)
    hours = RNG.choice(np.arange(24), n, p=hour_weights / hour_weights.sum())
    weather = RNG.choice(["clear","rain","fog"], n, p=[.65,.25,.10])
    severities = RNG.choice(["fatal","serious","minor","damage_only"], n, p=[.08,.25,.47,.20])
    vehicles = ["car","truck","bus","two_wheeler","auto_rickshaw","bicycle","pedestrian"]
    rows=[]
    for i, (_, s) in enumerate(sampled.iterrows(),1):
        v1=RNG.choice(vehicles,p=[.22,.10,.06,.45,.08,.04,.05]); v2=RNG.choice(vehicles,p=[.27,.12,.06,.29,.12,.07,.07])
        rows.append({"accident_id":i,"segment_id":int(s.segment_id),"lat":s.lat_start+RNG.normal(0,.0005),"lon":s.lon_start+RNG.normal(0,.0005),"severity":severities[i-1],"date":dates[i-1].strftime("%Y-%m-%d"),"time_of_day":f"{hours[i-1]:02d}:{int(RNG.integers(0,60)):02d}","day_of_week":dates[i-1].day_name(),"weather":weather[i-1],"vehicle_type_1":v1,"vehicle_type_2":v2,"num_casualties":int(RNG.choice([0,1,2,3],p=[.25,.49,.19,.07]))})
    return pd.DataFrame(rows)

if __name__ == "__main__":
    DATA.mkdir(exist_ok=True); roads=create_segments(); crashes=create_accidents(roads)
    roads.to_csv(DATA/"road_segments.csv",index=False); crashes.to_csv(DATA/"accidents.csv",index=False)
    print(f"Wrote {len(roads)} road segments and {len(crashes)} accidents to {DATA}")
