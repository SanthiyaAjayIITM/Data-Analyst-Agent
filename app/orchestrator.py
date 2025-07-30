import re
from typing import Dict, Tuple, Optional

import app.scraper as scraper_module
from app.duckdb_client import query_duckdb
from app.highcourt import get_most_active_court, compute_delay_slope
import app.plotter as plotter_module
from app.analyzer import compute_correlation


def extract_plot_columns(text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    From text like "Plot Rank vs Peak...", extract ("Rank", "Peak").
    """
    low = text.lower()
    idx = low.find(" vs ")
    if idx == -1:
        return None, None
    left = text[:idx].strip()
    right = text[idx + 4 :].strip()
    x_col = left.split()[-1] if left else None
    y_col = right.split()[0] if right else None
    return x_col, y_col


def parse_task(question_text: str) -> Dict[str, str]:
    """
    Determine task type and param.
    """
    text = question_text.lower()

    # 1. Scrape if keyword 'scrape' present
    if "scrape" in text:
        m = re.search(r'https?://[^\s]+', question_text)
        url = m.group(0) if m else ""
        return {"task_type": "scrape", "param": url}

    # 2. Query if SQL keywords present
    if any(kw in text for kw in ("select ", "from ", "where ")):
        return {"task_type": "query", "param": question_text.strip()}

    # 3. Plot if mentions plot or scatter
    if "plot" in text or "scatter" in text:
        return {"task_type": "plot", "param": question_text.strip()}

    # 4. Fallback
    return {"task_type": "unknown", "param": ""}

from functools import lru_cache

@lru_cache(maxsize=128)
def ask_llm_to_parse(question_text: str) -> Dict[str, str]:
    """
    Placeholder for future LLM parsing.
    """
    return parse_task(question_text)


def handle_task(question_text: str) -> dict:
    """
    Parse the question, then dispatch to the correct executor.
    """
    parsed = ask_llm_to_parse(question_text)

    # Scrape path
    if parsed["task_type"] == "scrape":
        try:
            df = scraper_module.scrape_wikipedia_table(parsed["param"])

            # 1) Film‑analysis path
            if "film" in question_text.lower():
                from app.analyzer import compute_correlation
                count_2bn = int(((df["Worldwide"] >= 2_000_000_000) & (df["Year"] < 2020)).sum())
                df15 = df[df["Worldwide"] >= 1_500_000_000]
                earliest = df15.loc[df15["Year"].idxmin(), "Title"] if not df15.empty else ""
                corr = compute_correlation(df, "Rank", "Peak")
                return {
                    "echo": question_text,
                    **parsed,
                    "count_2bn_before_2020": count_2bn,
                    "earliest_over_1.5bn": earliest,
                    "rank_peak_corr": corr,
                }

            # 2) Generic scrape path
            return {
                "echo": question_text,
                **parsed,
                "row_count": len(df),
                "columns": df.columns.tolist(),
            }
        except Exception as e:
            return {
                "echo": question_text,
                "task_type": parsed["task_type"],
                "error": str(e)
            }

    # Query path
    if parsed["task_type"] == "query":
        try:
            text = question_text.lower()

            # 1) Most active court question
            if "disposed the most cases" in text:
                court = get_most_active_court(2019, 2022)
                return {"echo": question_text, **parsed, "most_active_court": court}

            # 2) Delay slope by court
            if "regression slope" in text:
                # extract court_code from param or text
                m = re.search(r"court=([\w_]+)", text)
                code = m.group(1) if m else parsed["param"]
                slope = compute_delay_slope(code)
                return {"echo": question_text, **parsed, "delay_slope": slope}

            # 3) Generic SQL flow
            df = query_duckdb(parsed["param"])
            return {"echo": question_text, **parsed, "row_count": len(df), "columns": df.columns.tolist()}
        except Exception as e:
            return {
                "echo": question_text,
                "task_type": parsed["task_type"],
                "error": str(e)
            }

    # Plot path
    if parsed["task_type"] == "plot":
        try:
            param = parsed.get("param", "")

            # Legacy semicolon‑format support (for tests)
            if ";" in param and all(
                c.isdigit() or c in ",.;" for c in param.replace(" ", "")
            ):
                xs, ys = param.split(";")
                x_vals = [float(v) for v in xs.split(",") if v]
                y_vals = [float(v) for v in ys.split(",") if v]
                img = plotter_module.scatter_with_regression(x_vals, y_vals, "x", "y")
                return {"echo": question_text, **parsed, "image": img}

            # Real‑data plotting
            x_col, y_col = extract_plot_columns(question_text)
            if not x_col or not y_col:
                raise ValueError("Could not extract columns for plot")

            df = scraper_module.scrape_wikipedia_table(parsed["param"])
            if x_col not in df.columns or y_col not in df.columns:
                raise ValueError(f"Columns {x_col!r} or {y_col!r} not found in data")

            x_vals = df[x_col].astype(float).tolist()
            y_vals = df[y_col].astype(float).tolist()
            img = plotter_module.scatter_with_regression(x_vals, y_vals, x_col, y_col)
            return {"echo": question_text, **parsed, "image": img}
        except Exception as e:
            return {
                "echo": question_text,
                "task_type": parsed["task_type"],
                "error": str(e)
            }

    # Fallback echo
    return {"echo": question_text, **parsed}
