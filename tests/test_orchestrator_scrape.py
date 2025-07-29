import pandas as pd
from app.orchestrator import handle_task

def test_handle_task_scrape(monkeypatch):
    # 1. Stub parse to force task_type == scrape
    monkeypatch.setattr(
        "app.orchestrator.ask_llm_to_parse",
        lambda text: {"task_type": "scrape", "param": "http://example.com/foo"}
    )

    # 2. Stub scraper to return a small DataFrame
    df_fake = pd.DataFrame({"X": [10, 20]})
    monkeypatch.setattr(
        "app.scraper.scrape_wikipedia_table",
        lambda url: df_fake
    )

    res = handle_task("Scrape this URL")
    # Check routing fields
    assert res["task_type"] == "scrape"
    assert res["param"] == "http://example.com/foo"

    # Check scraper output mapping
    assert res["row_count"] == 2
    assert res["columns"] == ["X"]
    assert res["echo"] == "Scrape this URL"

def test_handle_task_scrape_bad_url(monkeypatch):
    # 1. Force parse to scrape
    monkeypatch.setattr(
        "app.orchestrator.ask_llm_to_parse",
        lambda t: {"task_type": "scrape", "param": "not-a-url"}
    )
    # 2. Stub scraper to raise
    monkeypatch.setattr(
        "app.scraper.scrape_wikipedia_table",
        lambda url: (_ for _ in ()).throw(ValueError("Invalid URL"))
    )
    # 3. Call and assert
    res = handle_task("Scrape this invalid link")
    assert res["task_type"] == "scrape"
    assert "error" in res
    assert "invalid url" in res["error"].lower()
