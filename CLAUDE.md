# CLAUDE.md

## Project overview

**ask-christian** is a RAG-powered Streamlit chatbot that answers questions about Christian Grøtteland based on his CV. Users can ask about skills, experience, and projects; the app retrieves relevant CV chunks from ChromaDB and passes them to Claude as context.

## Running the app

```bash
streamlit run app.py
```

On first load, `app.py` automatically calls `ingest()` if the session hasn't been initialized yet (`st.session_state.ingested`). The ChromaDB collection is persistent, so subsequent page reloads skip re-ingestion.

To re-ingest manually (e.g. after updating `docs/cv.txt`):

```bash
python src/ingest.py
```

## File structure

```
app.py              # Streamlit entry point — UI and session state
src/
  ingest.py         # Reads cv.txt, chunks it, stores in ChromaDB
  query.py          # Retrieves top-5 chunks, calls Claude API, returns answer
docs/
  cv.txt            # Source of truth — plain text CV (English + Norwegian)
  CV_Christian-Grøtteland-NO.pdf  # Original PDF (not directly used at runtime)
chroma_db/          # Persistent vector store (gitignored, recreated on ingest)
.streamlit/
  secrets.toml      # ANTHROPIC_API_KEY for Streamlit Cloud (gitignored)
.env                # ANTHROPIC_API_KEY for local dev (gitignored)
```

## API key setup

The API key is resolved in priority order in `src/query.py:8`:

1. `st.secrets["ANTHROPIC_API_KEY"]` — used on Streamlit Cloud (via `.streamlit/secrets.toml`)
2. `os.environ["ANTHROPIC_API_KEY"]` — used locally (via `.env` with `python-dotenv`)

## Common tasks

**Update CV content** — edit `docs/cv.txt`, then delete `chroma_db/` and re-run `python src/ingest.py`. The old ChromaDB collection will otherwise accumulate duplicate chunk IDs on the next ingest (chunk IDs are deterministic integers, so duplicates are silently overwritten, but it's cleaner to wipe first).

**Change the system prompt / persona** — edit the f-string in `src/query.py:31`. The prompt currently pins the date to April 2026 and describes Christian's current employment situation; update those lines when circumstances change.

**Adjust chunking** — `src/ingest.py:14`. `chunk_size=500` (characters) with `overlap=50`. ChromaDB uses its own embedding model (default all-MiniLM-L6-v2 via sentence-transformers) for similarity search — no external embedding API call.

**Change the Claude model** — `src/query.py:26`. Currently `claude-sonnet-4-6`.

## What's gitignored

- `.env` — local API key
- `.streamlit/secrets.toml` — Streamlit Cloud API key
- `chroma_db/` — regenerated from `docs/cv.txt` on ingest
- `venv/`, `.venv/` — Python virtual environments
- `__pycache__/`

## No test suite

There are no automated tests. Manual testing is done by running the app and querying it.
