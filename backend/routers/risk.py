from fastapi import APIRouter, HTTPException, Request
from models.schemas import RiskRequest, BatchRequest, RiskPrediction
from services.risk_calculator import risk_category, condition_delta
router=APIRouter(prefix="/api/risk",tags=["risk"])
@router.post("/predict",response_model=RiskPrediction)
def predict(payload: RiskRequest, request: Request):
    segment=request.app.state.store.segment(payload.segment_id)
    if not segment: raise HTTPException(404,"Segment not found")
    score,factors=request.app.state.predictor.predict(segment,payload.conditions.model_dump())
    return RiskPrediction(segment_id=payload.segment_id,risk_score=score,risk_category=risk_category(score),contributing_factors=factors)
@router.post("/batch")
def batch(payload: BatchRequest, request: Request):
    conditions=payload.conditions.model_dump(); result=[]
    for item in request.app.state.store.predictions["segments"]:
        copy=dict(item); score=min(100,round(item["risk_score_base"]+condition_delta(conditions),1)); copy["risk_score"]=score; copy["risk_category"]=risk_category(score); result.append(copy)
    return result
