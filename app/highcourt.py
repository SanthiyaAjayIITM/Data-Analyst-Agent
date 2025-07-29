import duckdb
import pandas as pd
import numpy as np  # Add this import



S3_PATH = "s3://indian-high-court-judgments/metadata/parquet/year=*/court=*/bench=*/metadata.parquet?s3_region=ap-south-1"

def get_most_active_court(start_year: int, end_year: int) -> str:
    """
    Returns the court_code that has the highest count of judgements
    between start_year and end_year (inclusive).
    """
    con = duckdb.connect(database=":memory:")
    con.execute("INSTALL httpfs; LOAD httpfs;")
    con.execute("INSTALL parquet; LOAD parquet;")
    sql = f"""
      SELECT court_code, COUNT(*) AS cnt
      FROM read_parquet('{S3_PATH}')
      WHERE year BETWEEN {start_year} AND {end_year}
      GROUP BY court_code
      ORDER BY cnt DESC
      LIMIT 1
    """
    df = con.execute(sql).df()
    con.close()
    return df.at[0, "court_code"] if not df.empty else ""

def compute_delay_slope(court_code: str) -> float:
    """
    For a given court_code, computes slope of 
    (decision_date - registration_date) in days vs year.
    """
    con = duckdb.connect(database=":memory:")
    con.execute("INSTALL httpfs; LOAD httpfs;")
    con.execute("INSTALL parquet; LOAD parquet;")
    sql = f"""
      SELECT year,
             (CAST(decision_date AS DATE) - CAST(date_of_registration AS DATE))::INTEGER AS delay
      FROM read_parquet('{S3_PATH}')
      WHERE court_code = '{court_code}'
    """
    df = con.execute(sql).df()
    con.close()
    # regression slope
    if len(df) < 2:
        return float("nan")
    slope, _ = np.polyfit(df["year"], df["delay"], 1)
    return float(slope)
