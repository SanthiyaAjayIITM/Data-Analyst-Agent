from fastapi import FastAPI
from app.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI(
    title="Data Analyst Agent",
    version="0.1.0",
    description="API for orchestrating data analysis tasks via LLM, scraping, DuckDB, and plotting"
)

# mount our routes
app.include_router(api_router, prefix="/api")