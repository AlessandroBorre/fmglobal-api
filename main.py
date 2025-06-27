
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import fitz  # PyMuPDF
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os

API_KEY = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)

# Preparazione dei documenti
def load_and_index(pdf_folder: str):
    docs = []
    for fname in os.listdir(pdf_folder):
        if not fname.endswith('.pdf'):
            continue
        path = os.path.join(pdf_folder, fname)
        text = ''
        with fitz.open(path) as pdf:
            for page in pdf:
                text += page.get_text()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(text)
        for chunk in chunks:
            docs.append(Document(page_content=chunk, metadata={"source": fname}))
    store = FAISS.from_documents(docs, embeddings)
    return store

# Carica all'avvio
documents = load_and_index('pdfs')

app = FastAPI(title="FM Global Query API")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@app.post("/query", response_model=QueryResponse)
async def query_docs(req: QueryRequest):
    query = req.question
    results = documents.similarity_search(query, k=3)
    answer = "".join([f"Source: {r.metadata['source']}\n{r.page_content}\n---\n" for r in results])
    return QueryResponse(answer=answer)
