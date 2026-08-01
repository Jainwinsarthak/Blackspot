from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from config import APP_NAME, MODEL_DIR
from data.loader import DataStore
from models.predictor import Predictor
from routers import risk,segments,simulate
app=FastAPI(title=APP_NAME,version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=False,allow_methods=["*"],allow_headers=["*"])
@app.on_event("startup")
def load_assets(): app.state.store=DataStore(); app.state.predictor=Predictor(MODEL_DIR)
app.include_router(risk.router); app.include_router(segments.router); app.include_router(simulate.router)
@app.get("/api/health")
def health(request:Request): return {"status":"ok","model_loaded":hasattr(request.app.state,"predictor"),"segments_count":len(request.app.state.store.segments)}
@app.get("/api/summary")
def summary(request:Request): return request.app.state.store.predictions["summary"]
@app.get("/api/shap/{segment_id}")
def shap(segment_id:int,request:Request):
    segment=request.app.state.store.segment(segment_id)
    if not segment: from fastapi import HTTPException; raise HTTPException(404,"Segment not found")
    _,factors=request.app.state.predictor.predict(segment,{})
    return {"segment_id":segment_id,"values":factors}
