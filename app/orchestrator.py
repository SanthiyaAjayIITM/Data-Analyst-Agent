import re
from typing import Dict
from app.scraper import scrape_wikipedia_table
from app.duckdb_client import query_duckdb

def parse_task(question_text: str) -> Dict[str, str]:
    """
    Rudimentary parser that inspects the question text
    and returns a dict with:
      - task_type: one of ["scrape", "query", "plot", "unknown"]
      - param: e.g. URL for scraping or SQL for query (empty if unknown)
    """
    text = question_text.lower()

    # Scrape if it mentions wikipedia URL
    url_match = re.search(r'(https?://\S+)', question_text)
    if url_match:
        url = url_match.group(1)
        return {"task_type": "scrape", "param": url}

    # DuckDB/SQL query if it contains SQL keywords
    if any(kw in text for kw in ("select ", "from ", "where ")):
        return {"task_type": "query", "param": question_text.strip()}

    # Plot if it mentions "plot" or "scatter"
    if "plot" in text or "scatter" in text:
        return {"task_type": "plot", "param": question_text.strip()}

    return {"task_type": "unknown", "param": ""}
    

def handle_task(question_text: str) -> dict:
    """
    Parse the question, then (for now) echo back the detection.
    """
    parsed = ask_llm_to_parse(question_text)
    
    if parsed["task_type"] == "scrape":
        # For scraping, fetch the table and return it
        df = scrape_wikipedia_table(parsed["param"])
        return {
            "echo": question_text,
            **parsed,
            "row_count": len(df),
            "columns": df.columns.tolist()
        }

    if parsed["task_type"] == "query":
        # For queries, run the SQL and return the DataFrame
        df = query_duckdb(parsed["param"])
        return {
            "echo": question_text,
            **parsed,
            "row_count": len(df),
            "columns": df.columns.tolist()
        }    
    
    # fallback for other task types
    return {"echo": question_text, **parsed}

def ask_llm_to_parse(question_text: str) -> Dict[str, str]:
    """
    Placeholder for LLM-based parsing.
    Later, this will call OpenAI ChatCompletion to get
    structured task_type & param.
    """
    # For now, just defer to our regex parser:
    return parse_task(question_text)
