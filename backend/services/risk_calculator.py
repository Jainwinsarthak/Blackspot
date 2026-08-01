def risk_category(score: float) -> str:
    if score >= 80: return "critical"
    if score >= 60: return "high"
    if score >= 35: return "medium"
    return "low"

def condition_delta(conditions: dict) -> float:
    weather = conditions.get("weather", "clear"); time = conditions.get("time", "day")
    return (13 if weather == "rain" else 18 if weather == "fog" else 0) + (12 if time in {"night","dawn","dusk"} else 0) + (11 if conditions.get("festival") else 0)
