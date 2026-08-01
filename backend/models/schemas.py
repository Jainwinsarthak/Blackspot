from pydantic import BaseModel, Field, field_validator

class Condition(BaseModel):
    weather: str = "clear"
    time: str = "day"
    festival: bool = False
    @field_validator("weather")
    @classmethod
    def valid_weather(cls, value):
        if value not in {"clear", "rain", "fog"}: raise ValueError("weather must be clear, rain, or fog")
        return value
    @field_validator("time")
    @classmethod
    def valid_time(cls, value):
        if value not in {"day", "night", "dawn", "dusk"}: raise ValueError("time must be day, night, dawn, or dusk")
        return value
class Intervention(BaseModel):
    segment_id: int
    interventions: list[str] = Field(default_factory=list)
    conditions: Condition = Field(default_factory=Condition)
class RiskRequest(BaseModel):
    segment_id: int
    conditions: Condition = Field(default_factory=Condition)
class BatchRequest(BaseModel): conditions: Condition = Field(default_factory=Condition)
class RiskPrediction(BaseModel):
    segment_id: int; risk_score: float; risk_category: str; contributing_factors: list[dict]
class SegmentDetail(BaseModel):
    segment_id: int; name: str; lat_start: float; lon_start: float; lat_end: float; lon_end: float
    road_type: str; risk_score: float; risk_category: str; features: dict; shap_values: list[dict]
    historical_accidents: int; what_if_results: dict
class CitySummary(BaseModel):
    total_segments: int; critical_count: int; high_count: int; medium_count: int; low_count: int
    total_accidents: int; top_factors: list[dict]
