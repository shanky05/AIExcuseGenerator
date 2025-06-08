from dotenv import load_dotenv
load_dotenv()


from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader


embeddings = OpenAIEmbeddings()

def search_documents(query: str, k=3):
    db = FAISS.load_local("data/embeddings", embeddings, allow_dangerous_deserialization=True)
    docs = db.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]
