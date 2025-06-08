from fastapi import APIRouter
from pydantic import BaseModel
from rag_engine import generate_excuse

router = APIRouter()

class ExcuseRequest(BaseModel):
    context: str
    persona: str = "professional"  # or "student", "parent", etc.

@router.post("/generate_excuse/")
async def get_excuse(req: ExcuseRequest):
    excuse = generate_excuse(req.context, req.persona)
    return {"excuse": excuse}

