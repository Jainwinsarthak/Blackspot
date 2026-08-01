"""API-safe wrapper around the canonical ML feature transformations."""
from pathlib import Path
import sys, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "ml"))
from feature_engineering import FEATURES, build_features as batch_features
def build_features(segment: dict, conditions: dict | None = None) -> pd.DataFrame:
    return batch_features(pd.DataFrame([segment]), conditions)
