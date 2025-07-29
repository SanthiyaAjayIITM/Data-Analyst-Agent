import pandas as pd
import numpy as np
from app.highcourt import get_most_active_court, compute_delay_slope
from app.orchestrator import handle_task

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

def test_handle_task_highcourt_sql_fail(monkeypatch):
    # 1. Force parse to query+highcourt most active
    monkeypatch.setattr(
        "app.orchestrator.ask_llm_to_parse",
        lambda t: {"task_type": "query", "param": ""}
    )
    # 2. Stub get_most_active_court to raise
    monkeypatch.setattr(
        "app.orchestrator.get_most_active_court",
        lambda s,e: (_ for _ in ()).throw(RuntimeError("DuckDB down"))
    )
    # 3. Call and assert
    res = handle_task("Which high court disposed the most cases from 2019 - 2022?")
    assert res["task_type"] == "query"
    assert "error" in res
    assert "duckdb down" in res["error"].lower()
