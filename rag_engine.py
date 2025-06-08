from langchain.adapters import openai

from vectorstore import search_documents
from prompts import build_prompt
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def generate_excuse(context: str, persona: str):
    docs = search_documents(context)
    prompt = build_prompt(context, docs, persona)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

