from dotenv import load_dotenv
from langchain.adapters import openai
from openai import OpenAI
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def generate_document_from_excuse(context: str, persona: str, excuse_text: str, filename="proofs/medical_note.pdf"):
    system_prompt = (
        "You are a professional doctor. Based on the user's excuse below, "
        "generate a formal, realistic medical certificate.\n\n"
       f"Excuse: {excuse_text}\n\n"
        f"Context: {context}\n"
        f"Persona: {persona}"
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": system_prompt}]
    )

    note_text = response.choices[0].message.content.strip()

    os.makedirs("proofs", exist_ok=True)

    # PDF setup
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    left_margin = inch
    top_margin = inch
    max_width = width - 2 * inch

    # Set font
    c.setFont("Helvetica", 12)

    # Text wrap
    from reportlab.platypus import Frame, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet

    styles = getSampleStyleSheet()
    paragraph = Paragraph(note_text.replace('\n', '<br/>'), styles['Normal'])

    frame = Frame(left_margin, height - top_margin - 500, max_width, 500, showBoundary=0)
    frame.addFromList([paragraph], c)

    c.save()
    return filename
