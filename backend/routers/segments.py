from fastapi import APIRouter, HTTPException, Query, Request
from services.risk_calculator import risk_category
router=APIRouter(prefix="/api/segments",tags=["segments"])
@router.get("")
def list_segments(request: Request, city: str="delhi", risk_min: float=Query(0,ge=0,le=100), risk_max: float=Query(100,ge=0,le=100), road_type: str="all"):
    records=[]
    for item in request.app.state.store.predictions["segments"]:
        if risk_min<=item["risk_score_base"]<=risk_max and (road_type=="all" or item["road_type"]==road_type): records.append(item)
    return records
@router.get("/{segment_id}")
def detail(segment_id:int,request:Request):
    segment=request.app.state.store.segment(segment_id)
    if not segment: raise HTTPException(404,"Segment not found")
    score,factors=request.app.state.predictor.predict(segment,{})
    item=request.app.state.store.by_id[segment_id]
    return {"segment_id":segment_id,"name":segment["name"],"lat_start":segment["lat_start"],"lon_start":segment["lon_start"],"lat_end":segment["lat_end"],"lon_end":segment["lon_end"],"road_type":segment["road_type"],"risk_score":score,"risk_category":risk_category(score),"features":segment,"shap_values":factors,"historical_accidents":len(request.app.state.store.crashes(segment_id)),"accidents":request.app.state.store.crashes(segment_id),"what_if_results":item["what_if"]}
