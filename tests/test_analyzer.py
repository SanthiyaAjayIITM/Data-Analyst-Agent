import pandas as pd
from app.analyzer import compute_correlation

def test_compute_correlation():
    df = pd.DataFrame({"A":[1,2,3], "B":[2,4,6]})
    corr = compute_correlation(df, "A", "B")
    # Perfect linear correlation → 1.0
    assert abs(corr - 1.0) < 1e-6
