# Loom Script — Handbook AI Capstone

Target length: **5–10 minutes**. Speak naturally; this is a guide, not a script to read word-for-word.

**Before you hit Record**

1. API running: `python -m uvicorn src.api:app --reload`
2. n8n running + workflow **Published**
3. Discord channel open
4. Browser tabs ready: http://127.0.0.1:8000/docs , n8n canvas, Discord, GitHub repo

---

## 1. Introduction (40–60 seconds)

**Say:**
> Hi, I'm [Your Name]. For the Capstone I extended my handbook RAG assistant so it can answer student questions using two knowledge sources: the Student Handbook PDF and the ZAIO website.
>
> When someone asks a question, the system retrieves the most relevant chunks from both sources, generates an answer with an LLM, and cites either a handbook page or a website URL. If the information isn't available, it refuses instead of inventing an answer.
>
> I also connected the API to n8n so a question can be accepted, sent to the RAG API, and forwarded to Discord.

**Show:** GitHub repo / project folder briefly.

---

## 2. Knowledge base pipeline (1–1.5 minutes)

**Show:** `CAPSTONE.md` or code files (`web_crawler.py`, `ingest.py`).

**Say:**
> Part 1 was extending the knowledge base. The assistant still loads the handbook PDF, extracts and chunks it with page numbers. For the website, I crawl selected ZAIO pages, clean out navigation and footer noise, then chunk that text too.
>
> All chunks are embedded with Sentence Transformers and stored in one ChromaDB collection, with metadata for source, page, and URL.

**Optional show:** Terminal snippet of `python src/ingest.py` output (collection count).

---

## 3. Live API demos (2.5–3.5 minutes)

**Show:** http://127.0.0.1:8000/docs or PowerShell.

### A) Handbook question

Ask: `When are the live classes?`

**Say:**
> This answer comes from the handbook. The source format is “Student Handbook - Page …” as required.

### B) Website question

Ask: `What courses does ZAIO offer?`

**Say:**
> This comes from the website knowledge. The source is a ZAIO URL.

### C) Unanswerable question

Ask: `What is the cafeteria pizza topping?`

**Say:**
> Here the assistant refuses with the Capstone message: it could not find that information in the available knowledge base. Source is null.

### D) Invalid request (Part 5 / API quality)

Send `{}` or empty question → show JSON error / 400.

**Say:**
> Invalid requests are handled gracefully with a clear JSON error, so n8n won't crash on bad input.

---

## 4. n8n workflow (2–3 minutes)

**Show:** Full n8n canvas.

**Say:**
> This is the Capstone n8n workflow. A webhook receives the question, we validate it, call the RAG API at POST /ask, notify Discord, and return JSON to the caller.

### Live demo

Run PowerShell:

```powershell
Invoke-RestMethod -Method POST -Uri "http://localhost:5678/webhook/handbook-ask" -ContentType "application/json" -Body '{"question":"What courses does ZAIO offer?"}' | ConvertTo-Json
```

**Show:**
1. JSON response in PowerShell  
2. Same answer appearing in Discord  

**Say:**
> So the workflow accepts the question, hits the API, gets the generated answer, and forwards it to Discord.

---

## 5. Tests & deliverables (45–60 seconds)

**Show:** Terminal `python -m pytest -q` (39 passed) and `TEST-RESULTS.md`.

**Say:**
> I have unit tests covering chunking, cleaning, retrieval, API validation, and dual-source metadata. Manual test results are documented with handbook questions, website questions, and unanswerable questions.

**Show:** Repo contains source, requirements, README, tests, test results, and n8n JSON.

---

## 6. Close (20–30 seconds)

**Say:**
> To summarise: dual-source RAG over the handbook and ZAIO website, a FastAPI /ask endpoint with proper citations, refusal when information is missing, automated tests, and an n8n path into Discord. Thanks for watching.

---

## Timing checklist

| Section | Approx. |
|---------|---------|
| Intro | 1 min |
| Knowledge base | 1–1.5 min |
| API demos | 3 min |
| n8n + Discord | 2–3 min |
| Tests / close | 1–1.5 min |
| **Total** | **~8–10 min** |
