from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
from langchain.docstore.document import Document
import json
import os

def load_doctors():
    with open("data/doctors.json") as f:
        return json.load(f)

def build_doctor_index(doctors):
    docs = [Document(page_content=doc["description"], metadata=doc) for doc in doctors]
    embeddings = OllamaEmbeddings(model="mistral")  # Uses local Ollama
    return FAISS.from_documents(docs, embeddings)

def find_best_doctor(symptoms: str, index):
    results = index.similarity_search(symptoms, k=1)
    if not results:
        return None
    return results[0].metadata
