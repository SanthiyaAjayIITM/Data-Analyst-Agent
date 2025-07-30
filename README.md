# Data Analyst Agent

A modular FastAPI application that orchestrates data analysis tasks via LLM parsing, web scraping, DuckDB querying, and plotting. Perfect for ad-hoc natural-language data analysis.

---

## 📦 Architecture Overview

```txt
Client → FastAPI (/api) → Orchestrator
  ├─ scrape → `app.scraper.scrape_wikipedia_table`
  ├─ query  → `app.duckdb_client.query_duckdb`
  ├─ plot   → `app.plotter.scatter_with_regression`
  ├─ film   → (`scrape` + `app.analyzer.compute_correlation` + extra logic)
  └─ highcourt → `app.highcourt.get_most_active_court`, `compute_delay_slope`
```

* **Parsing**: `ask_llm_to_parse` (regex + LLM stub)
* **Scraping**: Pandas `read_html` for Wikipedia tables
* **Querying**: DuckDB with HTTPFS/parquet on S3
* **Plotting**: Matplotlib scatter + dotted regression line, base64-encoded

---

## 🚀 Setup

### Prerequisites

* Python 3.10+
* [Docker](https://www.docker.com/) (optional, for containerized run)
* AWS credentials if querying S3-backed high-court data

### Local (venv)

```bash
git clone https://github.com/SanthiyaAjayIITM/Data-Analyst-Agent.git
cd Data-Analyst-Agent
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker

```bash
docker-compose up --build
# Server at http://localhost:8000
```

---

## 🔑 Environment Variables

| Name                    | Description                           | Example   |
| ----------------------- | ------------------------------------- | --------- |
| `OPENAI_API_KEY`        | OpenAI API key for LLM calls (future) | `sk-...`  |
| `AWS_ACCESS_KEY_ID`     | AWS S3 access key (highcourt)         | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | AWS S3 secret key                     | `...`     |

---

## 📝 API Endpoints

### Health Check

```http
GET /api/health HTTP/1.1
Host: localhost:8000
```

**Response**

```json
{ "status": "ok" }
```

### Task Endpoint

```http
POST /api/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{ "question_text": "<your natural-language task>" }
```

**Common Response Fields**

* `echo`: original question text
* `task_type`: one of `"scrape"`, `"query"`, `"plot"`, etc.

**Example: Scrape Films**

```bash
curl -X POST http://localhost:8000/api/ \
  -H 'Content-Type: application/json' \
  -d '{"question_text": "Analyze highest grossing films from https://en.wikipedia.org/wiki/List_of_highest-grossing_films"}'
```

**Sample JSON**

```json
{
  "echo": "Analyze highest grossing films from https://...",
  "task_type": "scrape",
  "param": "https://...",
  "count_2bn_before_2020": 2,
  "earliest_over_1.5bn": "Avatar",
  "rank_peak_corr": 0.72
}
```

**Example: High Court Query**

```bash
curl -X POST http://localhost:8000/api/ \
  -H 'Content-Type: application/json' \
  -d '{"question_text": "Which high court disposed the most cases from 2019 - 2022?"}'
```

**Sample JSON**

```json
{
  "echo": "Which high court disposed...",
  "task_type": "query",
  "param": "",
  "most_active_court": "33_10"
}
```

---

## 🎯 Next Steps

* Integrate real OpenAI LLM for advanced parsing & analysis
* Add persistent caching (Redis) for large S3 queries
* Implement API-key authentication and rate limiting

---

© 2025 Data Analyst Agent. MIT License.
