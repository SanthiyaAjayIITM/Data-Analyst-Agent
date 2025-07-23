import pandas as pd
from app.duckdb_client import query_duckdb

def test_query_duckdb(monkeypatch):
    # Fake DuckDB connect
    class FakeCon:
        def execute(self, sql):
            return self
        def df(self):
            return pd.DataFrame({"A":[1,2,3]})
        def close(self):
            pass

    monkeypatch.setattr("duckdb.connect", lambda database: FakeCon())

    df = query_duckdb("SELECT * FROM foo")
    assert isinstance(df, pd.DataFrame)
    assert list(df["A"]) == [1,2,3]
