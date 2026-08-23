# n8n Workflow — Handbook AI Capstone (Part 5)

This workflow:

1. Accepts a user question (`POST` webhook)
2. Sends it to your RAG API (`POST /ask`)
3. Forwards the answer to Discord
4. Returns JSON to the caller

## Prerequisites

1. FastAPI running locally:

```powershell
cd C:\Users\rejoi\Projects\handbook-ai-assistant
.\.venv\Scripts\Activate.ps1
python -m uvicorn src.api:app --reload
```

2. n8n running locally:

```powershell
npx n8n
```

Open http://localhost:5678

3. A Discord webhook URL  
   Discord channel → Edit Channel → Integrations → Webhooks → New Webhook → Copy URL

## Import the workflow

1. In n8n: **⋯** → **Import from File**
2. Choose `n8n/handbook-ask-workflow.json`
3. Open **Notify Discord**
4. Replace `REPLACE_WITH_YOUR_DISCORD_WEBHOOK_URL` with your real Discord webhook URL
5. Confirm **Call RAG API** URL is `http://127.0.0.1:8000/ask`  
   (If n8n runs in Docker, use `http://host.docker.internal:8000/ask`)
6. **Activate** the workflow
7. Copy the **Production** webhook URL from **Receive Question**

## Test

```powershell
Invoke-RestMethod -Method POST -Uri "http://localhost:5678/webhook/handbook-ask" -ContentType "application/json" -Body '{"question":"What courses does ZAIO offer?"}' | ConvertTo-Json
```

Expected:

- JSON response with `answer` + `source`
- Discord message with the same answer/source

Invalid body:

```powershell
Invoke-RestMethod -Method POST -Uri "http://localhost:5678/webhook/handbook-ask" -ContentType "application/json" -Body '{}' 
```

Should return an error JSON from n8n validation.

## Rubric mapping

| Requirement | Node |
|-------------|------|
| Accept user's question | Receive Question (Webhook) |
| Send question to RAG API | Call RAG API |
| Receive generated response | Call RAG API response |
| Present / forward response | Respond Success + Notify Discord |
