from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


# Load and embed documents
loader = TextLoader("data/docs/sample_docs.txt")  # Or use a folder with multiple files
docs = loader.load()


embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
db = FAISS.from_documents(docs, embeddings)

# Save the vector index
db.save_local("data/embeddings")

print("✅ Vector index created and saved.")
