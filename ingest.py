import os
from dotenv import load_dotenv
from pypdf import PdfReader
import chromadb

load_dotenv()

# Load the PDF
def load_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
        return text
    
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
    text = load_pdf("docs/CV_Christian-Grøtteland-NO.pdf")

    print("Chunking text...")
    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks")
    
    print("Storing in ChromaDB...")
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection(name="cv")
    
    collection.add(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
    
    print("Done! CV ingested successfully.")

if __name__ == "__main__":
    ingest()