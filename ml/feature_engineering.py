"""Repeatable feature transformations shared by training and API scoring."""
from __future__ import annotations
import pandas as pd

FEATURES = [
    "road_curvature_radius_m", "road_width_m", "lane_count", "speed_limit_kmh",
    "surface_quality", "elevation_change_m", "sight_distance_m", "road_type_encoded",
    "junction_complexity", "has_signal", "has_pedestrian_crossing", "has_median",
    "has_streetlight", "has_speed_breaker", "road_width_to_lane_ratio",
    "school_within_200m", "hospital_within_500m", "bus_stop_within_100m",
    "commercial_density", "population_density", "avg_rainfall_mm", "fog_days_per_year",
    "is_night", "is_rain", "is_festival",
]
ROAD_TYPES = {"residential": 0, "collector": 1, "arterial": 2, "highway": 3}

def build_features(segments: pd.DataFrame, conditions: dict | None = None) -> pd.DataFrame:
    """Produce the 25 model features; condition inputs are optional for baseline scoring."""
    conditions = conditions or {}
    frame = segments.copy()
    frame["surface_quality"] = frame["surface"].map({"unpaved": 0, "paved": 1}).fillna(1)
    frame["road_type_encoded"] = frame["road_type"].map(ROAD_TYPES).fillna(0)
    frame["road_width_to_lane_ratio"] = frame["road_width_m"] / frame["lane_count"].clip(lower=1)
    weather, time = conditions.get("weather", "clear"), conditions.get("time", "day")
    frame["is_night"] = int(time in {"night", "dawn", "dusk"})
    frame["is_rain"] = int(weather == "rain")
    frame["is_festival"] = int(bool(conditions.get("festival", False)))
    return frame.reindex(columns=FEATURES, fill_value=0).fillna(0)
