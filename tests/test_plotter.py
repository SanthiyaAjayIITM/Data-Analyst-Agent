from app.plotter import scatter_with_regression

def test_scatter_with_regression():
    # Simple linear data
    x = [0, 1, 2]
    y = [0, 1, 2]
    uri = scatter_with_regression(x, y, "X", "Y")
    assert uri.startswith("data:image/png;base64,")
    # Basic sanity: length should not be absurdly large
    assert len(uri) < 100_000
