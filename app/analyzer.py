import pandas as pd

def compute_correlation(
    df: pd.DataFrame, col_x: str, col_y: str
) -> float:
    """
    Return the Pearson correlation coefficient between col_x and col_y.
    """
    return float(df[col_x].corr(df[col_y]))
