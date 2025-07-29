import pandas as pd
from app.orchestrator import handle_task

def test_handle_task_query(monkeypatch):
    # Stub parsing
    monkeypatch.setattr(
        "app.orchestrator.ask_llm_to_parse",
        lambda text: {"task_type": "query", "param": "SELECT 1 AS one"}
    )
    # Stub query function
    df_fake = pd.DataFrame({"one":[1]})
    monkeypatch.setattr(
        "app.duckdb_client.query_duckdb",
        lambda sql: df_fake
    )

    res = handle_task("Run query")
    assert res["task_type"] == "query"
    assert res["param"] == "SELECT 1 AS one"
    assert res["row_count"] == 1
    assert res["columns"] == ["one"]
    assert res["echo"] == "Run query"

def test_handle_task_query_sql_fail(monkeypatch):
    # 1. Force parse to query
    monkeypatch.setattr(
        "app.orchestrator.ask_llm_to_parse",
        lambda t: {"task_type": "query", "param": "SELECT * FROM missing"}
    )
    # 2. Stub query to raise
    monkeypatch.setattr(
        "app.duckdb_client.query_duckdb",
        lambda sql: (_ for _ in ()).throw(Exception("SQL error"))
    )
    # 3. Call and assert
    res = handle_task("Run bad SQL")
    assert res["task_type"] == "query"
    assert "error" in res
    assert "error" in res["error"].lower()
