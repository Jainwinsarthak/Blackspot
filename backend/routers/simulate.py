from fastapi import APIRouter, HTTPException, Request
from models.schemas import Intervention
from services.whatif_engine import simulate_intervention
router=APIRouter(prefix="/api/simulate",tags=["simulation"])
@router.post("/whatif")
def whatif(payload:Intervention,request:Request):
    segment=request.app.state.store.segment(payload.segment_id)
    if not segment: raise HTTPException(404,"Segment not found")
    return simulate_intervention(segment,payload.interventions,request.app.state.predictor,payload.conditions.model_dump())
