from pathlib import Path
import json, pandas as pd
from config import DATA_DIR
class DataStore:
    def __init__(self):
        self.segments=pd.read_csv(DATA_DIR/"road_segments.csv").set_index("segment_id",drop=False)
        self.accidents=pd.read_csv(DATA_DIR/"accidents.csv")
        self.predictions=json.loads((DATA_DIR/"predictions.json").read_text(encoding="utf-8"))
        self.by_id={item["segment_id"]:item for item in self.predictions["segments"]}
    def segment(self, segment_id: int) -> dict | None:
        if segment_id not in self.segments.index:return None
        return self.segments.loc[segment_id].to_dict()
    def crashes(self, segment_id: int) -> list[dict]: return self.accidents[self.accidents.segment_id==segment_id].to_dict(orient="records")
