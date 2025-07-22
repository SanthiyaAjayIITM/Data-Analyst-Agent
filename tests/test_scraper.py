import pandas as pd
from app.scraper import scrape_wikipedia_table

def test_scrape_wikipedia_table(monkeypatch):
    # Prepare a fake DataFrame
    df_fake = pd.DataFrame({"A": [1, 2, 3]})

    # Monkeypatch pandas.read_html to return our fake table
    def fake_read_html(url):
        assert url == "http://example.com/test"  # ensure correct URL passed
        return [df_fake]

    monkeypatch.setattr("pandas.read_html", fake_read_html)

    # Call scraper
    df = scrape_wikipedia_table("http://example.com/test")
    pd.testing.assert_frame_equal(df, df_fake)
