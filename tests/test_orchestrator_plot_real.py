import pandas as pd
from app.orchestrator import handle_task

def test_handle_task_plot_real(monkeypatch):
    # 1. Stub parse to plot type
    monkeypatch.setattr(
        "app.orchestrator.ask_llm_to_parse",
        lambda text: {"task_type": "plot", "param": "http://example.com/table"}
    )
    # 2. Stub column extraction
    monkeypatch.setattr(
        "app.orchestrator.extract_plot_columns",
        lambda text: ("A", "B")
    )
    # 3. Stub scraper to return DataFrame with those cols
    df_fake = pd.DataFrame({"A":[1,2], "B":[3,4]})
    monkeypatch.setattr(
        "app.scraper.scrape_wikipedia_table",
        lambda url: df_fake
    )
    # 4. Stub plotter to capture inputs
    called = {}
    def fake_plot(x, y, xl, yl):
        called.update(x=x, y=y, xl=xl, yl=yl)
        return "data:image/png;base64,FAKE"
    monkeypatch.setattr(
        "app.plotter.scatter_with_regression",
        fake_plot
    )

    res = handle_task("Plot A vs B from example")
    assert res["task_type"] == "plot"
    assert res["image"] == "data:image/png;base64,FAKE"
    assert called["x"] == [1.0, 2.0]
    assert called["y"] == [3.0, 4.0]
    assert called["xl"] == "A"
    assert called["yl"] == "B"

def test_handle_task_plot_real_bad_df(monkeypatch):
    # 1. Force parse to plot
    monkeypatch.setattr(
        "app.orchestrator.ask_llm_to_parse",
        lambda t: {"task_type": "plot", "param": "http://example.com/table"}
    )
    # 2. Stub extract_plot_columns to valid cols
    monkeypatch.setattr(
        "app.orchestrator.extract_plot_columns",
        lambda t: ("X", "Y")
    )
    # 3. Stub scraper to return DF missing those cols
    monkeypatch.setattr(
        "app.scraper.scrape_wikipedia_table",
        lambda url: pd.DataFrame({"Z":[1,2,3]})
    )
    # 4. Call and assert
    res = handle_task("Plot X vs Y from table")
    assert res["task_type"] == "plot"
    assert "error" in res
    assert "not found in data" in res["error"].lower()
