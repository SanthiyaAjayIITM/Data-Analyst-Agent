from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.orchestrator import handle_task

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
async def handle_task_endpoint(req: TaskRequest):
    """
    Receive the question text, delegate to orchestrator.handle_task,
    and return its result.
    """
    # For now, just echo back an empty result
    try:
        result = handle_task(req.question_text)
        return TaskResponse(result=result)
    except Exception as e:
        # In future, refine error handling
        raise HTTPException(status_code=500, detail=str(e))