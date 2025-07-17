from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health_check():
    """
    Simple health check to confirm the service is up
    """
    return {"status": "ok"}

# Example placeholder POST endpoint
class TaskRequest(BaseModel):
    question_text: str

class TaskResponse(BaseModel):
    result: dict

@router.post("/", response_model=TaskResponse, tags=["Tasks"])
async def handle_task(request: TaskRequest):
    """
    Placeholder: receive the question text, and return an empty result.
    We'll implement this tomorrow.
    """
    # For now, just echo back an empty result
    return TaskResponse(result={})