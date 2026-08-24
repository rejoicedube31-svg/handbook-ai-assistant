# Handbook AI Assistant (Capstone)

RAG assistant that answers ZAIO student questions from **two** knowledge sources:

1. Student Handbook PDF  
2. ZAIO website — https://www.zaio.io  

If the answer is not in either source, it returns exactly:

> I could not find that information in the available knowledge base.

**Stack:** Python · Sentence Transformers · ChromaDB · OpenAI · FastAPI · BeautifulSoup · n8n  

**Branch:** `capstone`  
**Repo:** https://github.com/rejoicedube31-svg/handbook-ai-assistant

---

## Rubric coverage

| Part | Requirement | Deliverable |
|------|-------------|-------------|
| 1 | Extend knowledge base (PDF + website crawl/clean/chunk/embed) | `src/web_*`, `knowledge_base.py`, `ingest.py`, ChromaDB |
| 2 | Retrieve across sources; answer from context only; refuse if missing | `retrieve.py`, `generate.py`, `ask.py` |
| 3 | `POST /ask` with handbook page **or** website URL as `source` | `src/api.py` |
| 4 | Manual tests + unit tests | `TEST-RESULTS.md`, `tests/` (39 tests) |
| 5 | n8n: question → API → Discord | `n8n/handbook-ask-workflow.json` |

---

## Project layout

```text
handbook-ai-assistant/
├── data/
│   ├── handbook.pdf           # local only (gitignored)
│   └── website_clean.json     # crawl output (gitignored)
├── chroma_db/                 # vector store (gitignored)
├── src/
│   ├── web_config.py          # ZAIO seed URLs
│   ├── web_crawler.py         # crawl pages
│   ├── web_cleaner.py         # remove nav/header/footer noise
│   ├── pdf_loader.py          # load handbook PDF
│   ├── text_cleanup.py        # fix spaced PDF text
│   ├── chunking.py            # unified chunks + metadata
│   ├── knowledge_base.py      # combine handbook + website
│   ├── embeddings.py          # Sentence Transformers
│   ├── vectorstore.py         # ChromaDB store/search
│   ├── retrieve.py            # dual-source retrieval
│   ├── generate.py            # LLM answer / refuse
│   ├── ask.py                 # CLI RAG path
│   ├── ingest.py              # embed + store all chunks
│   └── api.py                 # FastAPI POST /ask
├── tests/                     # unit tests
├── n8n/
│   ├── handbook-ask-workflow.json
│   └── README.md
├── TEST-RESULTS.md
├── LOOM-SCRIPT.md
├── CAPSTONE.md
├── requirements.txt
└── README.md
```

---

## Setup

```powershell
cd C:\Users\rejoi\Projects\handbook-ai-assistant
git checkout capstone
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
```

1. Place the handbook at `data\handbook.pdf`
2. Set `OPENAI_API_KEY` in `.env`

---

## Build the knowledge base

```powershell
python src/web_crawler.py   # crawl + clean ZAIO pages
python src/ingest.py        # chunk, embed, store in one Chroma DB
```

Metadata stored per chunk:

- `source`: `Handbook` or `Website`
- `page`: handbook page number (when applicable)
- `url`: website URL (when applicable)

---

## Run the API

```powershell
python -m uvicorn src.api:app --reload
```

- Health: http://127.0.0.1:8000/
- Swagger docs: http://127.0.0.1:8000/docs

### `POST /ask`

**Request**

```json
{
  "question": "What courses does ZAIO offer?"
}
```

**Website-style response**

```json
{
  "answer": "...",
  "source": "https://www.zaio.io/"
}
```

**Handbook-style response**

```json
{
  "answer": "...",
  "source": "Student Handbook - Page 11"
}
```

**Not found**

```json
{
  "answer": "I could not find that information in the available knowledge base.",
  "source": null
}
```

**PowerShell**

```powershell
Invoke-RestMethod -Method POST -Uri http://127.0.0.1:8000/ask -ContentType "application/json" -Body '{"question":"When are the live classes?"}' | ConvertTo-Json
```

Invalid JSON / missing `question` → HTTP **400** with `{ "error": "..." }`.

---

## CLI (optional)

```powershell
python src/ask.py "When are the live classes?"
python src/ask.py "What courses does ZAIO offer?"
python src/ask.py "What is the cafeteria pizza topping?"
```

---

## Tests

```powershell
python -m pytest -q
```

Manual Q&A table (handbook / website / unanswerable): [`TEST-RESULTS.md`](TEST-RESULTS.md)

---

## n8n (Part 5)

Workflow file: [`n8n/handbook-ask-workflow.json`](n8n/handbook-ask-workflow.json)  
Setup guide: [`n8n/README.md`](n8n/README.md)

Flow: **Webhook → validate → POST /ask → Discord → JSON response**

---

## Loom demo

Speaking guide: [`LOOM-SCRIPT.md`](LOOM-SCRIPT.md) (target 5–10 minutes)

---

## Submit

Upload / share this GitHub repo (branch `capstone` or merge to `main` as required by your portal), including:

- Source code  
- `requirements.txt`  
- `README.md`  
- Unit tests  
- Test results  
- n8n workflow JSON  
- Loom video (5–10 minutes)
