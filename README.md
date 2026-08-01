# Handbook AI Assistant

RAG assistant that answers student questions from the Zaio handbook PDF.

**Stack:** Python · Sentence Transformers · ChromaDB · OpenAI · FastAPI

## Features (rubric)

| Part | Feature | Status |
|------|---------|--------|
| 1 | Load PDF, extract, chunk, embed, store in vector DB | Done |
| 2 | Retrieve relevant chunks and generate an LLM answer | Done |
| 3 | `POST /ask` JSON API | Done |
| 4 | Manual tests + unit tests | Done |
| 5 | JSON in/out + graceful invalid requests (n8n-ready) | Done |

## Project layout

```text
handbook-ai-assistant/
├── data/handbook.pdf     ← your handbook (gitignored)
├── chroma_db/            ← vector store (gitignored)
├── src/
│   ├── pdf_loader.py
│   ├── text_cleanup.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vectorstore.py
│   ├── retrieve.py
│   ├── generate.py
│   ├── ask.py
│   ├── ingest.py
│   └── api.py
├── tests/
├── TEST-RESULTS.md
├── requirements.txt
└── README.md
```

## Setup

```powershell
cd C:\Users\rejoi\Projects\handbook-ai-assistant
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
```

1. Put the handbook at `data\handbook.pdf`
2. Edit `.env` and set `OPENAI_API_KEY`

## Ingest the handbook

```powershell
python src/ingest.py
```

Creates embeddings and stores them in `chroma_db/`. Re-run after changing the PDF.

## Run the API

```powershell
python -m uvicorn src.api:app --reload
```

- Health: http://127.0.0.1:8000/
- Interactive docs: http://127.0.0.1:8000/docs

### `POST /ask`

Request:

```json
{
  "question": "When are the live classes?"
}
```

Response:

```json
{
  "answer": "Live classes are scheduled for Thursdays from 6 pm to 8 pm and Tuesdays from 9 am to 11 am for the first 12 weeks...",
  "source": "Page 11"
}
```

PowerShell example:

```powershell
Invoke-RestMethod -Method POST -Uri http://127.0.0.1:8000/ask -ContentType "application/json" -Body '{"question":"When are the live classes?"}' | ConvertTo-Json
```

Invalid request (missing `question`) returns HTTP 400:

```json
{
  "error": "Invalid request. Send JSON like {\"question\": \"Your question here\"}."
}
```

If the answer is not in the handbook, the assistant returns:

> I'm sorry, I don't have that information in the student handbook.

## CLI (optional)

```powershell
python src/ask.py "When is orientation day?"
```

## Tests

```powershell
python -m pytest -q
```

Manual Q&A table: see [TEST-RESULTS.md](TEST-RESULTS.md).

## Notes for markers / n8n

- API accepts and returns JSON only
- Invalid bodies are rejected with a clear JSON error (ready for the next n8n practical)
- `source` is `null` when the assistant cannot answer from the handbook
