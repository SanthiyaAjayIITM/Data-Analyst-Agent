import duckdb
import pandas as pd
import os

# Optionally read AWS creds from env:
# os.environ["AWS_ACCESS_KEY_ID"], etc.

def query_duckdb(sql: str) -> pd.DataFrame:
    """
    Runs the provided SQL (via DuckDB) and returns a DataFrame.
    Assumes httpfs is already installed/loaded.
    """
    con = duckdb.connect(database=":memory:")
    # Install and load httpfs & parquet
    con.execute("INSTALL httpfs; LOAD httpfs;")
    con.execute("INSTALL parquet; LOAD parquet;")
    # Execute the query
    df = con.execute(sql).df()
    con.close()
    return df
