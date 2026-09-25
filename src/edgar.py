import requests

HEADERS = {"User-Agent": "rayaghel@gmail.com"}
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"


def ticker_to_cik(ticker: str) -> str:
    response = requests.get(TICKERS_URL, headers=HEADERS)
    response.raise_for_status()

    companies = response.json()

    ticker_upper = ticker.upper()
    for entry in companies.values():
        if entry["ticker"] == ticker_upper:
            return str(entry["cik_str"]).zfill(10)

    raise ValueError(f"Ticker '{ticker}' not found in EDGAR company list")


def get_recent_filings(cik: str, n: int = 10) -> list[dict]:
    url = SUBMISSIONS_URL.format(cik=cik)
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    data = response.json()
    recent = data["filings"]["recent"]

    filings = []
    for i in range(min(n, len(recent["accessionNumber"]))):
        filings.append({
            "accession":  recent["accessionNumber"][i],
            "form":       recent["form"][i],
            "filed":      recent["filingDate"][i],
            "description": recent["primaryDocument"][i],
        })
    return filings


def get_document(cik: str, accession_number: str, filename: str) -> str:
    accession_clean = accession_number.replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_clean}/{filename}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text


if __name__ == "__main__":
    ticker = "TECK"
    cik = ticker_to_cik(ticker)
    print(f"{ticker} → CIK: {cik}")

    filings = get_recent_filings(cik)
    print(f"\nLast 10 filings for {ticker}:")
    for f in filings:
        print(f"  {f['filed']}  {f['form']:<10}  {f['description']}")

    # Retrieve the most recent document
    latest = filings[0]
    print(f"\nFetching most recent filing: {latest['description']}")
    html = get_document(cik, latest["accession"], latest["description"])
    print(html[:500])
