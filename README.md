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
- [ ] `POST /ask` API (Day 3)
- [ ] Tests + docs polish (Day 4)

## Setup

```powershell
cd C:\Users\rejoi\Projects\handbook-ai-assistant
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and set your `OPENAI_API_KEY`.

Put the handbook at `data\handbook.pdf`.

## Day 2 — ingest (embed + store)

```powershell
python src/ingest.py
```

First run may download the embedding model. You should see chunks stored in `chroma_db/`.

## Day 2 — ask a question

```powershell
python src/ask.py "What is the attendance requirement?"
python src/ask.py "What is the cafeteria pizza topping?"
```

The second question should return the not-available message (not in the handbook).
