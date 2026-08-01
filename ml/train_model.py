"""Train deterministic models and produce resilient static predictions."""
from __future__ import annotations
from pathlib import Path
import json, shutil
import joblib, pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from feature_engineering import FEATURES, build_features

ROOT=Path(__file__).resolve().parent; DATA=ROOT/"data"; BACKEND=ROOT.parent/"backend"/"ml"/"saved_models"
def category(score): return "critical" if score>=80 else "high" if score>=60 else "medium" if score>=35 else "low"
def main():
    roads=pd.read_csv(DATA/"road_segments.csv"); accidents=pd.read_csv(DATA/"accidents.csv")
    counts=accidents.groupby("segment_id").size().reindex(roads.segment_id,fill_value=0).to_numpy(); X=build_features(roads)
    y=(counts>pd.Series(counts).median()).astype(int)
    model=RandomForestClassifier(n_estimators=200,max_depth=12,min_samples_split=10,min_samples_leaf=5,class_weight="balanced",random_state=42).fit(X,y)
    reg=RandomForestRegressor(n_estimators=160,max_depth=12,min_samples_leaf=4,random_state=42).fit(X,counts)
    BACKEND.mkdir(parents=True,exist_ok=True); joblib.dump(model,BACKEND/"risk_classifier.joblib"); joblib.dump(reg,BACKEND/"risk_regressor.joblib")
    base=(model.predict_proba(X)[:,1]*100).round(1); imp=model.feature_importances_; ranked=sorted(zip(FEATURES,imp),key=lambda x:x[1],reverse=True)
    factors=[{"feature":f.replace("_"," ").title(),"importance":round(float(v),3)} for f,v in ranked[:8]]
    points=[]
    for pos, row in roads.iterrows():
        b=float(base[pos]); scores={"clear_day":b,"rain_day":min(100,b+13),"clear_night":min(100,b+12),"rain_night":min(100,b+27),"fog_morning":min(100,b+18),"festival_night":min(100,b+23)}
        points.append({"segment_id":int(row.segment_id),"lat":round((row.lat_start+row.lat_end)/2,6),"lon":round((row.lon_start+row.lon_end)/2,6),"name":row["name"],"risk_score_base":b,"risk_scores":scores,"risk_category":category(b),"top_factors":factors[:5],"what_if":{"add_signal":{"new_score":max(0,b-13),"delta":-13},"add_median":{"new_score":max(0,b-19),"delta":-19},"add_streetlight":{"new_score":max(0,b-10),"delta":-10},"add_speed_breaker":{"new_score":max(0,b-7),"delta":-7},"add_crossing":{"new_score":max(0,b-8),"delta":-8}},"historical_accidents":int(counts[pos]),"road_type":row.road_type,"lane_count":int(row.lane_count)})
    cats=pd.Series([p["risk_category"] for p in points]).value_counts()
    payload={"segments":points,"summary":{"total_segments":len(points),"critical_count":int(cats.get("critical",0)),"high_count":int(cats.get("high",0)),"medium_count":int(cats.get("medium",0)),"low_count":int(cats.get("low",0)),"total_accidents":int(len(accidents)),"top_city_factors":factors[:5]}}
    (DATA/"predictions.json").write_text(json.dumps(payload),encoding="utf-8")
    target=ROOT.parent/"frontend"/"src"/"data"; target.mkdir(parents=True,exist_ok=True); shutil.copy(DATA/"predictions.json",target/"predictions.json")
    print("Models trained. AUC (training-set diagnostic):",round(roc_auc_score(y,model.predict_proba(X)[:,1]),3))
if __name__=="__main__": main()
