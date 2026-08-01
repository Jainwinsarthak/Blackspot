from __future__ import annotations
from pathlib import Path
import joblib
from services.feature_engineer import build_features

class Predictor:
    def __init__(self, model_dir: Path):
        self.classifier = joblib.load(model_dir / "risk_classifier.joblib")
        self.regressor = joblib.load(model_dir / "risk_regressor.joblib")
        self.feature_names = list(self.classifier.feature_names_in_)
    def predict(self, segment: dict, conditions: dict | None = None) -> tuple[float, list[dict]]:
        features = build_features(segment, conditions)
        score = float(self.classifier.predict_proba(features)[0, 1] * 100)
        importances = self.classifier.feature_importances_
        values = features.iloc[0]
        factors = [{"feature": key.replace("_", " ").title(), "importance": round(float(weight), 3), "value": float(values[key])} for key, weight in sorted(zip(self.feature_names, importances), key=lambda item:item[1], reverse=True)[:8]]
        return round(score, 1), factors
