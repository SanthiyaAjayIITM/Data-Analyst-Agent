from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_film_analysis(monkeypatch):
    import pandas as pd

    mock_df = pd.DataFrame({
        "Rank": [1, 2],
        "Peak": [1, 2],
        "Title": ["Avatar", "Titanic"],
        "Worldwide gross": ["2,923,706,026", "2,257,844,554"],
        "Year": [2009, 1997],
        "Ref": ["", ""]
    })

    def mock_scrape_wikipedia_table(url):
        df = mock_df.copy()
        df["Worldwide gross"] = df["Worldwide gross"].str.replace(",", "").astype(float)
        return df

    monkeypatch.setattr("app.scraper.scrape_wikipedia_table", mock_scrape_wikipedia_table)

    response = client.post("/api/", json={
        "question_text": "Analyze highest grossing films from https://fake.com"
    })

    assert response.status_code == 200
    json_data = response.json()["result"]
    assert json_data["task_type"] == "scrape"
    assert isinstance(json_data["count_2bn_before_2020"], int)
    assert isinstance(json_data["rank_peak_corr"], float)
