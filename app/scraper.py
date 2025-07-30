# app/scraper.py

import pandas as pd

from functools import lru_cache

@lru_cache(maxsize=128)
def scrape_wikipedia_table(url: str) -> pd.DataFrame:
    """
    Fetch the first HTML table from the given Wikipedia URL
    and return it as a DataFrame.
    """
    # pandas.read_html will pull all tables and return a list
    tables = pd.read_html(url)
    if not tables:
        raise ValueError(f"No tables found at {url}")
    # Return the first table
    return tables[0]
