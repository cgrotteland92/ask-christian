# SPEC.md — ask-christian

## What it is

A personal portfolio chatbot that lets visitors ask natural-language questions about Christian Grøtteland. Instead of reading a static CV, visitors can ask things like "What programming languages does Christian know?" or "Has he led teams before?" and get a direct, grounded answer.

## Target user

Recruiters, hiring managers, or curious developers who land on Christian's portfolio and want a faster way to learn about him than reading a CV PDF.

## Core behaviour

- Answers are grounded strictly in the CV. If the information isn't in the CV, the bot says so honestly rather than hallucinating.
- The bot speaks in third person about Christian ("He has..."), not as Christian himself.
- Conversation history is preserved within a single browser session (via `st.session_state.messages`) but is not sent to the model — each question is answered independently using only the retrieved CV chunks as context.

## Architecture

```
User question
     │
     ▼
ChromaDB similarity search
(top 5 chunks from cv.txt)
     │
     ▼
Anthropic Claude API
(claude-sonnet-4-6, max_tokens=1024)
     │
     ▼
Answer displayed in Streamlit chat UI
```

### Ingestion pipeline

1. `docs/cv.txt` is read as plain UTF-8 text.
2. Text is split into overlapping character-level chunks (`chunk_size=500`, `overlap=50`).
3. Chunks are stored in a local ChromaDB persistent collection (`chroma_db/`, collection name `cv-data`).
4. ChromaDB embeds chunks automatically using its default embedding model (sentence-transformers `all-MiniLM-L6-v2`) — no external embedding API is used.

Ingestion runs automatically on the first Streamlit page load if the session hasn't been flagged as ingested yet. It can also be run standalone with `python src/ingest.py`.

### Query pipeline

1. The user's question is sent to ChromaDB as a query; the top 5 most similar chunks are returned.
2. The 5 chunks are joined with double newlines to form a context block.
3. A single user message is sent to Claude containing the system instructions, context block, and the question.
4. Claude's text response is returned and displayed.

## Tech stack

| Component | Choice | Reason |
|---|---|---|
| UI | Streamlit | Minimal boilerplate for a chat interface; fast to iterate |
| Vector DB | ChromaDB (persistent, local) | No external service needed; embeddings included |
| LLM | Anthropic Claude (`claude-sonnet-4-6`) | High quality, reliable API |
| CV source | Plain text (`docs/cv.txt`) | Simple to edit; avoids PDF parsing complexity at query time |

## Secrets and configuration

| Variable | Where | Used for |
|---|---|---|
| `ANTHROPIC_API_KEY` | `.env` (local) or `.streamlit/secrets.toml` (Streamlit Cloud) | Authenticating Claude API calls |

No other configuration is required. ChromaDB data is local and ephemeral (gitignored).

## Known limitations

- **No streaming** — Claude's full response is awaited before display; a spinner is shown in the meantime.
- **No multi-turn context to the model** — conversation history is shown in the UI but each model call sees only the retrieved chunks, not prior turns. This is intentional to keep the prompt focused and costs low.
- **Character-level chunking** — chunks split on character count, not sentence or paragraph boundaries, which can produce awkward mid-sentence splits. Semantic chunking would improve retrieval quality.
- **Duplicate ingestion** — re-running ingest without deleting `chroma_db/` overwrites chunks in place (IDs are deterministic) rather than erroring, but may leave stale chunks if the CV shrinks between runs.

## Deployment

The app is designed for deployment on **Streamlit Community Cloud**. The `ANTHROPIC_API_KEY` is set via Streamlit's secrets management UI, which writes to `.streamlit/secrets.toml` on the server.

`chroma_db/` is not committed to git, so ingestion must run on first startup. The auto-ingest logic in `app.py` handles this: it calls `ingest()` before rendering the UI, keyed on `st.session_state.ingested` to prevent repeat runs within a session.
