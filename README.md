# ask-christian 🤖

An AI-powered chatbot built over my own CV and portfolio using
Retrieval-Augmented Generation (RAG). Ask it anything about my
skills, experience, projects or background.

**Live demo:** [link here once deployed]

---

## How it works

Instead of relying on a pre-trained model's general knowledge,
this app uses RAG to ground every answer in my actual CV data:

1. **Ingestion** — CV is chunked and stored in a ChromaDB vector database
2. **Retrieval** — when you ask a question, the most relevant chunks are fetched
3. **Generation** — those chunks are sent to Claude as context, which generates an accurate answer

This means the AI only answers based on what's actually in my CV,
not hallucinated information.

---

## Tech stack

- Python
- Anthropic Claude API (claude-sonnet-4-6)
- ChromaDB (vector database)
- Streamlit (UI)
- pypdf / plain text ingestion

---

## Run locally

1. Clone the repo
2. Create a virtual environment and activate it

```bash
   python -m venv venv
   venv\Scripts\activate
```

3. Install dependencies

```bash
   pip install -r requirements.txt
```

4. Create a `.env` file with your Anthropic API key

5. Ingest the CV

```bash
   python src/ingest.py
```

6. Run the app

```bash
   streamlit run app.py
```

---
