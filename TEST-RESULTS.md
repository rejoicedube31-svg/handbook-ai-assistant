# Capstone Part 4 — Manual Test Results

These questions were run against the live Capstone assistant (`python src/ask.py` and/or `POST /ask`) using:

- Student Handbook PDF
- ZAIO website (https://www.zaio.io)

Exact not-found message used:

> I could not find that information in the available knowledge base.

| # | Question | Type | Retrieved Source | Generated Answer |
|---|----------|------|------------------|------------------|
| 1 | When are the live classes? | Handbook | Student Handbook - Page 11 | Live classes are Thursdays 6–8 pm and Tuesdays 9–11 am for the first 12 weeks; then one Tuesday class 9–11 am. |
| 2 | When is orientation day? | Handbook | Student Handbook - Page 7 | Orientation Day is on 15 January 2026 at 10 am. |
| 3 | What courses does ZAIO offer? | Website | https://www.zaio.io/ | ZAIO offers Full Stack AI Engineer, Cloud & DevOps Engineer, Fullstack Web Development, Data Science, Cybersecurity, and Digital Marketing bootcamps. |
| 4 | How flexible are the payment options? | Website | https://www.zaio.io/tuition-financing | Flexible options include instalments, upfront payment, and financing partners such as Manati and Capitec (including learn-now/pay-later style options). |
| 5 | What is the cafeteria pizza topping? | Unanswerable | N/A (`source: null`) | I could not find that information in the available knowledge base. |
| 6 | What is ZAIO's secret Mars campus address? | Unanswerable | N/A (`source: null`) | I could not find that information in the available knowledge base. |

## How to reproduce

```powershell
# Ensure knowledge base is built
python src/web_crawler.py
python src/ingest.py

# CLI tests
python src/ask.py "When are the live classes?"
python src/ask.py "What courses does ZAIO offer?"
python src/ask.py "What is the cafeteria pizza topping?"

# API (server must be running)
python -m uvicorn src.api:app --reload
Invoke-RestMethod -Method POST -Uri http://127.0.0.1:8000/ask -ContentType "application/json" -Body '{"question":"What courses does ZAIO offer?"}' | ConvertTo-Json
```

## Unit tests

```powershell
python -m pytest -q
```

Expected: **39 passed** (library warnings from FastAPI/Chroma are OK).
