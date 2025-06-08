from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os


def generate_medical_note_pdf(filename: str = "proofs/medical_note.pdf"):
    os.makedirs("proofs", exist_ok=True)

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Sample content
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 100, "To Whom It May Concern,")
    c.drawString(100, height - 130, "This is to certify that the individual named below was under my care")
    c.drawString(100, height - 150, "on the stated date due to medical reasons.")

    c.drawString(100, height - 190, f"Name: Shashank Shekhar")  # Later, make dynamic
    c.drawString(100, height - 210, f"Date: {datetime.today().strftime('%B %d, %Y')}")
    c.drawString(100, height - 230, f"Condition: Viral fever and advised rest")

    c.drawString(100, height - 270, "Doctor Signature:")
    c.line(200, height - 272, 350, height - 272)

    c.save()
    return filename
