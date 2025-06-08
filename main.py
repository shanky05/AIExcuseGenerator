from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import uuid
import os
from dotenv import load_dotenv

from rag_engine import generate_excuse
from generators.document_generator import generate_document_from_excuse
from routes import router

# Load environment variables
load_dotenv()

# Initialize app
app = FastAPI(title="AI Excuse Generator")

# Serve static PDFs
app.mount("/proofs", StaticFiles(directory="proofs"), name="proofs")

# Include routers
app.include_router(router)

# Allow CORS
origins = [
    "http://localhost:3000",                # local React
    "https://excuse-frontend.vercel.app"    # deployed React
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ExcuseRequest(BaseModel):
    context: str
    persona: str

# API route for excuse only
@app.post("/api/generate-excuse")
async def get_excuse(req: ExcuseRequest):
    excuse = generate_excuse(req.context, req.persona)
    return {"excuse": excuse}

# ✅ Corrected API route for excuse + proof
@app.post("/api/generate-excuse-with-proof")
async def generate_excuse_with_proof(req: ExcuseRequest, request: Request):  # <-- add `request` here
    # Step 1: Generate Excuse
    excuse = generate_excuse(req.context, req.persona)

    # Step 2: Generate PDF with that excuse
    filename = f"medical_note_{uuid.uuid4().hex}.pdf"
    file_path = os.path.join("proofs", filename)
    generate_document_from_excuse(
        excuse_text=excuse,
        context=req.context,
        persona=req.persona,
        filename=file_path
    )

    # Step 3: Use request.base_url to construct full URL
    base_url = str(request.base_url).rstrip("/")
    pdf_url = f"{base_url}/proofs/{filename}"

    return JSONResponse(content={
        "excuse": excuse,
        "pdf_url": pdf_url
    })
