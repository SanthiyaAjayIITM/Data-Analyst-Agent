from app.orchestrator import handle_task

def test_handle_task_plot(monkeypatch):
    # Stub parsing to return a simple two-series param
    monkeypatch.setattr(
        "app.orchestrator.ask_llm_to_parse",
        lambda text: {
            "task_type": "plot",
            "param": "0,1,2;0,1,2"
        }
    )
    # Stub plotter to return a known URI
    monkeypatch.setattr(
        "app.plotter.scatter_with_regression",
        lambda x, y, xl, yl: "data:image/png;base64,TEST"
    )


    res = handle_task("Plot this")
    assert res["task_type"] == "plot"
    assert res["param"] == "0,1,2;0,1,2"
    assert res["echo"] == "Plot this"
    assert res["image"] == "data:image/png;base64,TEST"

def test_handle_task_plot_column_fail(monkeypatch):
    # 1. Force parse to plot
    monkeypatch.setattr(
        "app.orchestrator.ask_llm_to_parse",
        lambda t: {"task_type": "plot", "param": "http://example.com"}
    )
    # 2. Stub extract_plot_columns to return no columns
    monkeypatch.setattr(
        "app.orchestrator.extract_plot_columns",
        lambda t: (None, None)
    )
    # 3. Call and assert
    res = handle_task("Plot without vs")
    assert res["task_type"] == "plot"
    assert "error" in res
    assert "could not extract columns" in res["error"].lower()
