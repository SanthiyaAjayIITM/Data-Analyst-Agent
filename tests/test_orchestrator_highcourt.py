from app.orchestrator import handle_task

def test_handle_task_most_active(monkeypatch):
    monkeypatch.setattr(
        "app.orchestrator.ask_llm_to_parse",
        lambda t: {"task_type":"query","param":""}
    )
    monkeypatch.setattr(
        "app.orchestrator.get_most_active_court",
        lambda start,end: "33_10"
    )
    res = handle_task("Which high court disposed the most cases from 2019 - 2022?")
    assert res["most_active_court"] == "33_10"

def test_handle_task_delay_slope(monkeypatch):
    monkeypatch.setattr("app.orchestrator.ask_llm_to_parse",
                        lambda t: {"task_type":"query","param":"33_10"})
    monkeypatch.setattr("app.orchestrator.compute_delay_slope",
                        lambda code: 5.5)
    res = handle_task("What's the regression slope of the date_of_registration - decision_date by year in the court=33_10?")
    assert abs(res["delay_slope"] - 5.5) < 1e-6
