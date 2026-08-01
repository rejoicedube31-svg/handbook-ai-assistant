# Part 4 — Manual Test Results

These questions were run against the live assistant (CLI and/or `POST /ask`) using the Zaio student handbook.

| # | Question | Source / Page | Answer (summary) |
|---|----------|---------------|------------------|
| 1 | When are the live classes? | Page 11 | Thursdays 6–8 pm and Tuesdays 9–11 am for the first 12 weeks; then one Tuesday class 9–11 am. |
| 2 | When is orientation day? | Page 7 | Orientation Day is on 15 January 2026 at 10 am. |
| 3 | Who do I contact for student success? | Page 15 | Suhana Patel (Student Success). |
| 4 | What is the attendance requirement? | N/A | Not available — handbook does not state a formal attendance %. |
| 5 | What is the cafeteria pizza topping? | N/A | Not available — not in the handbook (guardrail check). |

## How to reproduce

```powershell
# CLI
python src/ask.py "When are the live classes?"

# API (server must be running)
Invoke-RestMethod -Method POST -Uri http://127.0.0.1:8000/ask -ContentType "application/json" -Body '{"question":"When are the live classes?"}' | ConvertTo-Json
```

## Unit tests

```powershell
python -m pytest -q
```
