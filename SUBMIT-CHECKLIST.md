# Capstone Day 12 — Final Submit Checklist

**Due:** 29 August 2026  
**Target ready:** 28 August (1 day spare)  
**Branch:** `capstone`  
**Repo:** https://github.com/rejoicedube31-svg/handbook-ai-assistant

Verified locally: **39 unit tests passed**, key deliverable files present, branch clean vs `origin/capstone`.

---

## A. Rubric done?

| Part | Item | Done? |
|------|------|-------|
| 1 | Handbook PDF + ZAIO website in one vector DB with metadata | [x] |
| 2 | Retrieve across sources; refuse if missing | [x] |
| 3 | `POST /ask` returns handbook page or website URL | [x] |
| 4 | Manual tests + unit tests | [x] |
| 5 | n8n: question → API → Discord | [x] |

---

## B. GitHub package

Confirm these are on GitHub (`capstone` branch):

- [x] Source code (`src/`)
- [x] `requirements.txt`
- [x] `README.md`
- [x] Unit tests (`tests/`)
- [x] Test results (`TEST-RESULTS.md`)
- [x] n8n workflow (`n8n/handbook-ask-workflow.json`)
- [x] Loom script (`LOOM-SCRIPT.md`) — optional helper for recording

**Do not commit:** `.env`, `.venv/`, `chroma_db/`, `data/handbook.pdf`, Discord webhook URL

Quick check:

```powershell
git checkout capstone
git status
git push
```

Open the GitHub `capstone` branch in a browser and confirm files look right.

---

## C. Record the Loom (5–10 minutes)

Use [`LOOM-SCRIPT.md`](LOOM-SCRIPT.md).

**Before record**

```powershell
# Terminal 1
python -m uvicorn src.api:app --reload

# Terminal 2
npx n8n
```

- n8n workflow **Published**
- Discord channel open
- Tabs: `/docs`, n8n canvas, Discord, GitHub

**Must show on camera**

1. Handbook question → `Student Handbook - Page …`
2. Website question → `https://www.zaio.io/…`
3. Unanswerable → Capstone not-found message
4. n8n webhook → JSON + Discord message
5. Brief mention of tests / repo deliverables

Save the Loom link somewhere safe for the portal.

---

## D. Portal submit (by 29 Aug)

- [ ] Submit GitHub link (confirm if they want `capstone` branch or merge to `main`)
- [ ] Submit Loom video link
- [ ] Keep one spare day (28 Aug) for any portal/upload issues

### If the portal expects `main`

Only after Capstone is complete:

```powershell
git checkout main
git merge capstone
git push origin main
```

Or open a Pull Request: `capstone` → `main` on GitHub.

---

## E. Smoke test one last time (optional, 28 Aug)

```powershell
python -m pytest -q
python src/ask.py "When are the live classes?"
python src/ask.py "What courses does ZAIO offer?"
python src/ask.py "What is the cafeteria pizza topping?"
```
