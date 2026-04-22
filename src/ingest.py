import os
from dotenv import load_dotenv
from pypdf import PdfReader
import chromadb

load_dotenv()

# Load the PDF
def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
# Split text into chunks
def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

# Save chunks to ChromaDB
def ingest ():
    print("Ingesting...")
    text = load_txt("docs/cv.txt")

    print("Chunking text...")
    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks")
    
    print("Storing in ChromaDB...")
    client = chromadb.EphemeralClient()
    collection = client.get_or_create_collection(name="cv-data")

    collection.add(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

    print("Done! CV ingested successfully.")
    return collection

if __name__ == "__main__":
    ingest()