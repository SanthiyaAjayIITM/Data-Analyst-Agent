from app.orchestrator import extract_plot_columns

def test_extract_plot_columns_basic():
    text = "Please plot Rank vs Peak from this data"
    x, y = extract_plot_columns(text)
    assert x == "Rank"
    assert y == "Peak"

def test_extract_plot_columns_fail():
    text = "Generate a histogram"
    x, y = extract_plot_columns(text)
    assert x is None and y is None
