"""
Orchestrator: routes incoming question_text
to the correct data‑analysis function.
"""

def handle_task(question_text: str) -> dict:
    """
    TODO: parse question_text, decide whether to scrape,
    query DuckDB, compute metrics, or plot.
    For now, return a placeholder dict.
    """
    # Placeholder: echo back the question
    return {"echo": question_text}
