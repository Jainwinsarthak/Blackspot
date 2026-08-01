from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'backend'))
from services.risk_calculator import risk_category,condition_delta
def test_categories_and_conditions():
    assert risk_category(80)=='critical' and risk_category(34)=='low'
    assert condition_delta({'weather':'rain','time':'night','festival':False})>condition_delta({'weather':'clear','time':'day','festival':False})
