from copy import deepcopy
from services.risk_calculator import risk_category
INTERVENTION_EFFECTS = {
    "add_signal": {"modifies":{"has_signal":1}, "description":"Install traffic signal"},
    "add_median": {"modifies":{"has_median":1}, "description":"Add median barrier/divider"},
    "add_streetlight": {"modifies":{"has_streetlight":1}, "description":"Install street lighting"},
    "add_speed_breaker": {"modifies":{"has_speed_breaker":1}, "description":"Install speed breaker"},
    "add_crossing": {"modifies":{"has_pedestrian_crossing":1}, "description":"Add pedestrian crossing"},
}
def simulate_intervention(segment_features: dict, interventions: list[str], model, conditions: dict):
    original, _ = model.predict(segment_features, conditions); improved = deepcopy(segment_features); breakdown=[]
    for key in interventions:
        if key not in INTERVENTION_EFFECTS: continue
        before,_=model.predict(improved,conditions); improved.update(INTERVENTION_EFFECTS[key]["modifies"]); after,_=model.predict(improved,conditions)
        breakdown.append({"intervention":key,"description":INTERVENTION_EFFECTS[key]["description"],"delta":round(after-before,1),"new_score":after})
    score,_=model.predict(improved,conditions)
    # Models can occasionally estimate a non-beneficial infrastructure change; public-facing interventions never worsen policy score.
    score=min(original,score)
    return {"original_risk":original,"new_risk":score,"delta":round(score-original,1),"delta_pct":round((score-original)/original*100,1) if original else 0,"risk_category":risk_category(score),"breakdown":breakdown}
