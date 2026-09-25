# filing-agent

A multi-agent system for financial analysis of SEC-listed companies.

It separates two fundamentally different jobs: **deterministic data extraction** (numbers from EDGAR filings) and **qualitative analysis** (an LLM reasoning over those numbers). The two layers never mix — the LLM never touches raw filings, and the extraction layer never guesses.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Ingestion Layer                    │
│                  (deterministic)                     │
│                                                      │
│   SEC EDGAR API  →  FinancialFact (Pydantic)         │
│   - company_tickers.json  →  zero-padded CIK         │
│   - submissions endpoint  →  filing index            │
│   - XBRL facts API        →  validated numbers       │
└─────────────────────────┬───────────────────────────┘
                          │  clean, typed, validated
                          ▼
┌─────────────────────────────────────────────────────┐
│                  Computation Layer                   │
│                  (deterministic)                     │
│                                                      │
│   - Financial ratios  (P/E, debt/equity, margins)    │
│   - Period-over-period deltas                        │
│   - Peer comparisons                                 │
└─────────────────────────┬───────────────────────────┘
                          │  structured summary
                          ▼
┌─────────────────────────────────────────────────────┐
│                   Analysis Layer                     │
│                      (LLM)                           │
│                                                      │
│   - Interprets ratios and trends in plain language   │
│   - Flags anomalies and risks                        │
│   - Never receives raw filings or unvalidated data   │
└─────────────────────────────────────────────────────┘
```

**Why this separation matters:** LLMs are good at reasoning over structured summaries and writing clearly. They are unreliable at arithmetic and data extraction. Keeping them out of the numbers layer means the numbers are always auditable and the analysis is always grounded.

---

## Current status

| Component | Status |
|---|---|
| `ticker_to_cik(ticker)` | Done — fetches and zero-pads CIK from EDGAR |
| `get_recent_filings(cik)` | Done — returns last N filings with form type and date |
| `get_document(cik, accession, filename)` | Done — fetches raw filing HTML |
| `FinancialFact` Pydantic model | Done — validates XBRL financial data |
| XBRL facts ingestion | Next |
| Ratio computation | Upcoming |
| LLM analysis layer | Upcoming |

---

## Setup

```bash
git clone https://github.com/rayaghel/filing-agent.git
cd filing-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```python
from src.edgar import ticker_to_cik, get_recent_filings

cik = ticker_to_cik("TECK")
print(cik)  # 0000886986

filings = get_recent_filings(cik)
for f in filings:
    print(f["filed"], f["form"])
```

## Running tests

```bash
pytest -v
```

---

## SEC EDGAR API notes

- `User-Agent` header with name and email is **required** — requests without it return 403
- Rate limit: 10 requests/second
- CIK must be zero-padded to 10 digits in all API URLs
