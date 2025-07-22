from app.orchestrator import parse_task

def test_parse_scrape():
    q = "Scrape the list from https://en.wikipedia.org/wiki/List_of_foo"
    out = parse_task(q)
    assert out["task_type"] == "scrape"
    assert out["param"].startswith("https://en.wikipedia.org/wiki/List_of_foo")

def test_parse_query():
    q = "SELECT * FROM table WHERE year=2020"
    out = parse_task(q)
    assert out["task_type"] == "query"
    assert "select" in out["param"].lower()

def test_parse_plot():
    q = "Please plot the distribution of Rank vs Peak"
    out = parse_task(q)
    assert out["task_type"] == "plot"
    assert "plot" in out["param"].lower()

def test_parse_unknown():
    q = "How many movies grossed over $2bn?"
    out = parse_task(q)
    assert out["task_type"] == "unknown"
    assert out["param"] == ""
