from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'ml'))
from feature_engineering import FEATURES,build_features
def test_feature_count_and_edge_values():
    source={'road_curvature_radius_m':0,'road_width_m':8,'lane_count':0,'speed_limit_kmh':150,'surface':'paved','elevation_change_m':0,'sight_distance_m':1,'road_type':'residential','junction_complexity':2,'has_signal':0,'has_pedestrian_crossing':0,'has_median':0,'has_streetlight':0,'has_speed_breaker':0,'school_within_200m':0,'hospital_within_500m':0,'bus_stop_within_100m':0,'commercial_density':0,'population_density':0,'avg_rainfall_mm':0,'fog_days_per_year':0}
    x=build_features(__import__('pandas').DataFrame([source]),{'weather':'rain','time':'night','festival':True})
    assert list(x.columns)==FEATURES and len(x.columns)==25 and x.iloc[0].is_night==1
