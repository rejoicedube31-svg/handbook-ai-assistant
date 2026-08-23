# Capstone plan (branch: `capstone`)

Due: **29 Aug 2026** · Target ready: **28 Aug** (1 day spare)

## Day 1 status — done

- [x] Work on `capstone` branch (keeps `main` as previous submission)
- [x] Handbook PDF still loads (26 pages)
- [x] ZAIO crawl scope defined (seed URLs below)

## Day 2 status — done

- [x] Crawl seed URLs with `httpx` + BeautifulSoup
- [x] Extract title + text (script/style removed)
- [x] Save raw crawl to `data/website_raw.json` (gitignored)
- [x] Drop empty JS-shell routes from seed list (community, cloud-devops detail, refund)

## Day 3 status — done

- [x] Prefer `<main>` content; drop `header` / `footer` / `nav`
- [x] Strip leftover chrome phrases (newsletter, repeated footer)
- [x] Save cleaned pages to `data/website_clean.json`
- [x] Unit tests in `tests/test_web_cleaner.py`

## Day 4 status — done

- [x] Unified chunking for Handbook + Website
- [x] Metadata: `source`, `page` (handbook), `url` (website)
- [x] Combined output saved to `data/knowledge_chunks.json`

## Day 5 status — done

- [x] Embed handbook + website chunks into one Chroma collection
- [x] Store metadata: source, page, URL

## Day 6 status — done

- [x] Retrieve across handbook + website
- [x] Capstone not-found message
- [x] Source format: `Student Handbook - Page N` or website URL

## Day 7 status — done

- [x] Update `POST /ask` for Capstone response shapes
- [x] Health endpoint lists both knowledge sources
- [x] API tests for handbook URL / website / not-found

## Day 8 status — done

- [x] Broader Capstone unit tests (crawler, retrieve merge/boost, vectorstore roundtrip)

## Day 9 status — done

- [x] Manual test table: handbook, website, and unanswerable questions
- [x] Updated `TEST-RESULTS.md` with Question / Source / Answer
- [ ] n8n workflow (Day 10)


## Knowledge sources

| Source | Type | Metadata |
|--------|------|----------|
| Student Handbook | PDF `data/handbook.pdf` | `source=Handbook`, `page=N` |
| ZAIO website | https://www.zaio.io | `source=Website`, `url=...` |

## Website crawl scope (seed URLs)

Crawl these public pages first (enough for course / FAQ / financing questions). Skip login, external apps, and social links.

### Core
- https://www.zaio.io/
- https://www.zaio.io/bootcamps
- https://www.zaio.io/compare-courses
- https://www.zaio.io/tuition-financing
- https://www.zaio.io/aboutus
- https://www.zaio.io/community
- https://www.zaio.io/qualifications

### Bootcamp detail pages
- https://www.zaio.io/fullstack-ai-engineer-bootcamp
- https://www.zaio.io/cloud-devops-engineer-bootcamp
- https://www.zaio.io/fullstack-bootcamp
- https://www.zaio.io/datascience-bootcamp
- https://www.zaio.io/cybersecurity-bootcamp
- https://www.zaio.io/digital-marketing-bootcamp

### Useful extras
- https://www.zaio.io/company
- https://www.zaio.io/learner-stories
- https://www.zaio.io/events
- https://www.zaio.io/refundPolicy
- https://www.zaio.io/terms

### Out of scope (Day 2+)
- https://www.zaio.io/app/login (auth)
- https://applications.zaio.io/* (separate app)
- Social / Trustpilot / mailto links

## Exact not-found message (Capstone)

```text
I could not find that information in the available knowledge base.
```

## Remaining program

| Day | Date | Focus |
|-----|------|--------|
| 2 | 17 Aug | Crawl + extract website text |
| 3 | 18 Aug | Clean web content |
| 4 | 19 Aug | Unified chunks + metadata |
| 5 | 20 Aug | Embed into one Chroma DB |
| 6 | 21 Aug | Retrieve + refuse message + source format |
| 7 | 22 Aug | Update `POST /ask` |
| 8 | 23 Aug | Unit tests |
| 9 | 24 Aug | Manual test results |
| 10 | 25 Aug | n8n workflow |
| 11 | 26 Aug | README + export n8n JSON |
| 12 | 27 Aug | Loom 5–10 min |
| 13 | 28 Aug | Buffer / final push |
| — | 29 Aug | Due |
