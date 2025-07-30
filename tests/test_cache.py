import pandas as pd
import pytest

from app.orchestrator import ask_llm_to_parse, parse_task
from app.scraper import scrape_wikipedia_table

call_counts = {"parse": 0, "scrape": 0}

@pytest.fixture(autouse=True)
def reset_cache_and_counts(monkeypatch):
    # Reset counters
    call_counts["parse"] = 0
    call_counts["scrape"] = 0

    # Clear any existing cache
    ask_llm_to_parse.cache_clear()

    # Monkeypatch parse_task so we can count calls
    def counting_parse(q):
        call_counts["parse"] += 1
        # Delegate to real parser for correct behavior
        return parse_task.__wrapped__(q) if hasattr(parse_task, "__wrapped__") else parse_task(q)

    monkeypatch.setattr("app.orchestrator.parse_task", counting_parse)

    # Monkeypatch pandas.read_html for scraping
    def fake_read_html(url):
        call_counts["scrape"] += 1
        return [pd.DataFrame({"A": [1, 2, 3]})]

    monkeypatch.setattr("pandas.read_html", fake_read_html)
    # Clear scrape cache
    scrape_wikipedia_table.cache_clear()

    yield

def test_parse_cache():
    # First call: should invoke counting_parse -> count 1
    ask_llm_to_parse("Hello Cache")
    # Second call with same input: cache hit -> no extra parse_task call
    ask_llm_to_parse("Hello Cache")
    assert call_counts["parse"] == 1

def test_scrape_cache():
    # First call: should invoke fake_read_html -> count 1
    scrape_wikipedia_table("http://example.com")
    # Second call with same URL: cache hit -> no extra read_html
    scrape_wikipedia_table("http://example.com")
    assert call_counts["scrape"] == 1
