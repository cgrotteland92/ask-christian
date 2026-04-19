import os
from dotenv import load_dotenv
import chromadb
import anthropic

load_dotenv()

client = anthropic.Anthropic()
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_collection(name="cv-data")

def ask(question):
    # Retrieve relevant chunks from ChromaDB
    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    context = "\n\n".join(results["documents"][0])

      # Send to Claude with context
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are an assistant that answers questions about Christian based on his CV.
                
Use the following context from his CV to answer the question.
If the answer isn't in the context, say so honestly.

Context:
{context}

Question: {question}"""
            }
        ]
    )
    
    return message.content[0].text

# Simple chat loop
if __name__ == "__main__":
    print("Ask me anything about Christian! (type 'quit' to exit)\n")
    while True:
        question = input("You: ")
        if question.lower() == "quit":
            break
        answer = ask(question)
        print(f"\nAssistant: {answer}\n")