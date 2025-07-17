from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(
    title="Data Analyst Agent",
    version="0.1.0",
    description="A FastAPI application for a data analyst agent that can process and analyze data.",
)

app.include_router(api_router)