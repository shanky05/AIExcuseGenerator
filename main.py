
from pydantic import BaseModel

from generators.document_generator import generate_document_from_excuse
from rag_engine import generate_excuse
from routes import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from rag_engine import generate_excuse
from generators.document_generator import generate_document_from_excuse
import uuid
import os

app = FastAPI(title="AI Excuse Generator")

from fastapi.staticfiles import StaticFiles
app.mount("/proofs", StaticFiles(directory="proofs"), name="proofs")


app.include_router(router)

from dotenv import load_dotenv
load_dotenv()

origins = [
    "http://localhost:3000",               # for React dev mode
    "https://excuse-frontend.vercel.app/" # change this after deploying frontend
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,                # allow specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExcuseRequest(BaseModel):
    context: str
    persona: str  # Add this field to match function requirement

@app.post("/api/generate-excuse")
async def get_excuse(req: ExcuseRequest):
    excuse = generate_excuse(req.context, req.persona)  # Pass both args
    return {"excuse": excuse}

@app.post("/api/generate-excuse-with-proof")
async def generate_excuse_with_proof(req: ExcuseRequest):


    # Step 1: Generate Excuse
    excuse = generate_excuse(req.context, req.persona)

    # Step 2: Generate PDF with that excuse (use UUID for unique filename)
    filename = f"medical_note_{uuid.uuid4().hex}.pdf"
    file_path = os.path.join("proofs", filename)
    generate_document_from_excuse(context=req.context,
        persona=req.persona,excuse_text=excuse, filename=file_path)

    # Step 3: Return both excuse and file URL
    base_url = str(req.base_url).rstrip("/")
    pdf_url = f"{base_url}/proofs/{filename}"

    return JSONResponse(content={
        "excuse": excuse,
        "pdf_url": pdf_url
    })