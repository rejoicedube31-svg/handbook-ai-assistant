# Handbook AI Assistant

Answer student questions from the student handbook using RAG (retrieve → generate).

## Project layout

```text
handbook-ai-assistant/
├── data/           ← put handbook.pdf here
├── chroma_db/      ← created by ingest (gitignored)
├── src/            ← Python source
├── tests/          ← unit tests (later)
├── requirements.txt
└── README.md
```

## Progress

- [x] Repo + folders
- [x] Load PDF / extract text / chunk (Day 1)
- [x] Embeddings + ChromaDB + retrieve + LLM answer (Day 2)
- [x] `POST /ask` API (Day 3)
- [ ] Tests + docs polish (Day 4)

## Setup

```powershell
cd C:\Users\rejoi\Projects\handbook-ai-assistant
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and set your `OPENAI_API_KEY`.

Put the handbook at `data\handbook.pdf`.

## Ingest (required once, or after PDF changes)

```powershell
python src/ingest.py
```

## Run the API (Day 3)

```powershell
python -m uvicorn src.api:app --reload
```

Open docs: http://127.0.0.1:8000/docs

### Example request

```powershell
curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d "{\"question\": \"When are the live classes?\"}"
```

### Example response

```json
{
  "answer": "...",
  "source": "Page 11"
}
```

Invalid requests return JSON like:

```json
{
  "error": "Invalid request. Send JSON like {\"question\": \"Your question here\"}."
}
```

## CLI ask (Day 2)

```powershell
python src/ask.py "When are the live classes?"
python src/ask.py "What is the cafeteria pizza topping?"
```
