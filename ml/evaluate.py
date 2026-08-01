from pathlib import Path
import joblib, pandas as pd
from sklearn.metrics import classification_report, roc_auc_score
from feature_engineering import build_features
root=Path(__file__).resolve().parent; roads=pd.read_csv(root/'data/road_segments.csv'); crashes=pd.read_csv(root/'data/accidents.csv')
counts=crashes.groupby('segment_id').size().reindex(roads.segment_id,fill_value=0); y=(counts>counts.median()).astype(int); model=joblib.load(root.parent/'backend/ml/saved_models/risk_classifier.joblib'); p=model.predict_proba(build_features(roads))[:,1]
print('AUC-ROC:',round(roc_auc_score(y,p),3)); print(classification_report(y,p>=.5))
