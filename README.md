# Handbook AI Assistant

Answer student questions from the student handbook using RAG (retrieve → generate).

## Project layout

```text
handbook-ai-assistant/
├── data/           ← put handbook.pdf here
├── src/            ← Python source
├── tests/          ← unit tests (later)
├── requirements.txt
└── README.md
```

## Day 1 status

- [x] Repo + folders
- [x] Load PDF
- [x] Extract text (with page numbers)
- [x] Split into chunks
- [ ] Embeddings + vector DB (Day 2)
- [ ] `POST /ask` API (Day 3)
- [ ] Tests + docs polish (Day 4)

## Setup

```powershell
cd C:\Users\rejoi\Projects\handbook-ai-assistant
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Put the handbook in place

Copy your PDF to:

`data\handbook.pdf`

## Day 1 quick check

```powershell
python src/ingest.py
```

You should see page count, chunk count, and a few chunk previews with page numbers.
