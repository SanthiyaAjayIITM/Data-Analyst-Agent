import pandas as pd
import numpy as np
from app.highcourt import get_most_active_court, compute_delay_slope

def test_get_most_active_court(monkeypatch):
    # stub DuckDB connect
    class FakeCon:
        def execute(self, sql):
            class R:
                def df(inner):
                    return pd.DataFrame({"court_code": ["33_10"], "cnt":[100]})
            return R()
        def close(self): pass
    monkeypatch.setattr("duckdb.connect", lambda **kw: FakeCon())
    assert get_most_active_court(2019,2022) == "33_10"

def test_compute_delay_slope(monkeypatch):
    class FakeCon:
        def execute(self, sql):
            class R:
                def df(inner):
                    return pd.DataFrame({"year":[2019,2020,2021],"delay":[10,20,30]})
            return R()
        def close(self): pass
    monkeypatch.setattr("duckdb.connect", lambda **kw: FakeCon())
    slope = compute_delay_slope("33_10")
    # Perfect linear → slope ~10
    assert abs(slope - 10.0) < 1e-6
