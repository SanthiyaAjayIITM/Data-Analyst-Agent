import pandas as pd
from app.orchestrator import handle_task

def test_handle_task_film(monkeypatch):
    # 1. Stub parse to film scrape
    monkeypatch.setattr(
        "app.orchestrator.ask_llm_to_parse",
        lambda text: {"task_type":"scrape","param":"http://example.com/films"}
    )
    # 2. Stub scraper to return a fake film table
    df = pd.DataFrame({
        "Worldwide": [2_100_000_000, 1_600_000_000, 900_000_000],
        "Year": [2019, 2018, 2021],
        "Title": ["FilmA","FilmB","FilmC"],
        "Rank": [1, 2, 3],
        "Peak": [100, 80, 60],
    })
    monkeypatch.setattr(
        "app.scraper.scrape_wikipedia_table",
        lambda url: df
    )

    res = handle_task("Film analysis question")
    assert res["count_2bn_before_2020"] == 1         # only FilmA
    assert res["earliest_over_1.5bn"].lower().startswith("filmb")
    assert abs(res["rank_peak_corr"] - df["Rank"].corr(df["Peak"])) < 1e-6

def test_handle_task_film_missing_columns(monkeypatch):
    # 1. Force parse to scrape+film
    monkeypatch.setattr(
        "app.orchestrator.ask_llm_to_parse",
        lambda t: {"task_type": "scrape", "param": "http://example.com/films"}
    )
    # 2. Stub scraper to return DF without Worldwide/Year
    monkeypatch.setattr(
        "app.scraper.scrape_wikipedia_table",
        lambda url: pd.DataFrame({"X":[1,2,3]})
    )
    # 3. Call and assert
    res = handle_task("Film analysis question")
    assert res["task_type"] == "scrape"
    assert "error" in res
    assert "worldwide" in res["error"].lower() or "year" in res["error"].lower()
