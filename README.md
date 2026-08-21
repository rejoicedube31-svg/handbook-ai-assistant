# Handbook AI Assistant (Capstone)

RAG assistant that answers student questions from:
- the **Student Handbook** PDF
- the **ZAIO website** (https://www.zaio.io)

**Stack:** Python · Sentence Transformers · ChromaDB · OpenAI · FastAPI · BeautifulSoup

Branch: `capstone`

## Capstone features

| Part | Feature | Status |
|------|---------|--------|
| 1 | Handbook + website crawl/clean/chunk/embed in one vector DB | Done |
| 2 | Retrieve across both sources; refuse if not found | Done |
| 3 | `POST /ask` returns handbook page **or** website URL as `source` | Done |
| 4 | Unit tests + test results | In progress (Day 8–9) |
| 5 | n8n workflow | Day 10 |

## Project layout

```text
handbook-ai-assistant/
├── data/handbook.pdf          ← handbook (gitignored)
├── data/website_clean.json    ← cleaned crawl (gitignored)
├── chroma_db/                 ← vector store (gitignored)
├── src/
│   ├── web_crawler.py / web_cleaner.py / web_config.py
│   ├── knowledge_base.py
│   ├── pdf_loader.py, chunking.py, embeddings.py, vectorstore.py
│   ├── retrieve.py, generate.py, ask.py
│   ├── ingest.py
│   └── api.py
├── tests/
├── CAPSTONE.md
├── requirements.txt
└── README.md
```

## Setup

```powershell
cd C:\Users\rejoi\Projects\handbook-ai-assistant
git checkout capstone
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
```

1. Put the handbook at `data\handbook.pdf`
2. Edit `.env` and set `OPENAI_API_KEY`

## Build the knowledge base

```powershell
# Crawl + clean ZAIO website
python src/web_crawler.py

# Chunk handbook + website, embed, store in one Chroma DB
python src/ingest.py
```

## Run the API

```powershell
python -m uvicorn src.api:app --reload
```

- Health: http://127.0.0.1:8000/
- Docs: http://127.0.0.1:8000/docs

### `POST /ask`

Request:

```json
{
  "question": "What courses does ZAIO offer?"
}
```

Website response example:

```json
{
  "answer": "...",
  "source": "https://www.zaio.io/bootcamps"
}
```

Handbook response example:

```json
{
  "answer": "...",
  "source": "Student Handbook - Page 18"
}
```

Not found:

```json
{
  "answer": "I could not find that information in the available knowledge base.",
  "source": null
}
```

PowerShell:

```powershell
Invoke-RestMethod -Method POST -Uri http://127.0.0.1:8000/ask -ContentType "application/json" -Body '{"question":"What courses does ZAIO offer?"}' | ConvertTo-Json
```

Invalid request (missing `question`) → HTTP 400 JSON `error`.

## CLI

```powershell
python src/ask.py "When are the live classes?"
python src/ask.py "What courses does ZAIO offer?"
```

## Tests

```powershell
python -m pytest -q
```

## Notes for markers / n8n

- API accepts and returns JSON only
- Invalid bodies get a clear JSON error
- `source` is a handbook citation, a website URL, or `null` when not found
