import pytest
from app.orchestrator import handle_task

def test_handle_task_film_analysis(monkeypatch):
    # Mock DataFrame to simulate the scraped Wikipedia table
    import pandas as pd

    mock_df = pd.DataFrame({
        "Rank": [1, 2, 3],
        "Peak": [1, 1, 1],
        "Title": ["Avatar", "Avengers: Endgame", "Titanic"],
        "Worldwide gross": ["2,923,706,026", "2,797,800,564", "2,257,844,554"],
        "Year": [2009, 2019, 1997],
        "Ref": ["", "", ""]
    })

    def mock_scrape_wikipedia_table(url):
        df = mock_df.copy()
        df["Worldwide gross"] = df["Worldwide gross"].str.replace(",", "").astype(float)
        return df

    monkeypatch.setattr("app.scraper.scrape_wikipedia_table", mock_scrape_wikipedia_table)

    result = handle_task("Analyze highest grossing films from https://example.com")
    assert result["task_type"] == "scrape"
    assert result["count_2bn_before_2020"] == 3
    assert result["earliest_over_1.5bn"] == "Titanic"
    assert isinstance(result["rank_peak_corr"], float)
