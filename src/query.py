import os
import streamlit as st
from dotenv import load_dotenv
import chromadb
import anthropic

load_dotenv()
api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

def get_or_create_collection():
    chroma_client = chromadb.PersistentClient(path="chroma_db")
    return chroma_client.get_or_create_collection(name="cv-data")

def ask(question):
    collection = get_or_create_collection()
    
    results = collection.query(
        query_texts=[question],
        n_results=5
    )
    
    context = "\n\n".join(results["documents"][0])
    
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are an assistant that answers questions about Christian Grøtteland based on his CV.
The current date is April 2026. 
Christian currently works as a painter at Jærstil AS while actively searching for roles in AI development, frontend development or IT consulting in the Stavanger area.
All listed education is completed.

Use the following context from his CV to answer the question.
If the answer isn't in the context, say so honestly.

Context:
{context}

Question: {question}"""
            }
        ]
    )
    
    return message.content[0].text

if __name__ == "__main__":
    print("Ask me anything about Christian! (type 'quit' to exit)\n")
    while True:
        question = input("You: ")
        if question.lower() == "quit":
            break
        answer = ask(question)
        print(f"\nAssistant: {answer}\n")