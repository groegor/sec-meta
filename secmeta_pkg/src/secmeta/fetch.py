from __future__ import annotations
import requests, sys
import time
from typing import Dict, List, Iterator

BASE = "https://data.sec.gov/submissions/CIK{}.json"
COMPANY_KEYS = [
    "cik","name","sic","sicDescription","ein","category","fiscalYearEnd",
    "stateOfIncorporation","tickers","exchanges","phone"
]

def _get(url: str, ua: str) -> dict:
    r = requests.get(url, headers={"User-Agent": ua}, timeout=30)
    r.raise_for_status()
    return r.json()

def fetch_company_json(cik: str, ua: str) -> dict:
    return _get(BASE.format(cik), ua)

def _emit(js: dict, form_filter: str|None, cik_stripped: str):
    recent = js.get("filings", {}).get("recent", {})
    if not recent:
        return
    keys = list(recent.keys())
    length = len(recent["accessionNumber"])
    for idx in range(length):
        if form_filter and recent["form"][idx] != form_filter:
            continue
        row = {k: recent[k][idx] for k in keys}
        try:
            acc_raw = row["accessionNumber"].replace("-", "")
            file = row.get("primaryDocument", "")
            row["primaryDocumentUrl"] = (
                f"https://www.sec.gov/Archives/edgar/data/{cik_stripped}/{acc_raw}/{file}"
                if file else ""
            )
        except Exception:
            row["primaryDocumentUrl"] = ""
        yield row

def iter_filings(company_json: dict, ua: str, form_filter: str|None=None) -> Iterator[Dict]:
    cik_stripped = str(company_json["cik"]).lstrip("0")
    yield from _emit(company_json, form_filter, cik_stripped)
    for extra in company_json.get("files", []):
        js = _get("https://data.sec.gov/" + extra["name"], ua)
        yield from _emit(js, form_filter, cik_stripped)

def harvest(cik: str, ua: str, form_filter: str|None=None) -> List[Dict]:
    cj = fetch_company_json(cik, ua)
    company_meta = {k: cj.get(k, "") for k in COMPANY_KEYS}
    rows = []
    for filing in iter_filings(cj, ua, form_filter):
        combined = {**company_meta, **filing}
        rows.append(combined)
    return rows


# Acceptable forms in EDGAR
VALID_FORMS = {
    "DEF14A": "DEF 14A",
    "DEFA14A": "DEFA14A",
    "DEFM14A": "DEFM14A",
    "DEFR14A": "DEFR14A",
    "DEFN14A": "DEFN14A",
    "PRE14A": "PRE 14A",
    "10K": "10-K",
    "10Q": "10-Q",
    "8K": "8-K",
    "11K": "11-K",
    "S3ASR": "S-3ASR",
    "S8": "S-8",
    "FWP": "FWP",
    "144": "144",
    "4": "4",
    "4A": "4/A",
    "3": "3",
    "3A": "3/A",
    "SC13G": "SC 13G",
    "SC13GA": "SC 13G/A",
    "SCTOTTA": "SC TO-T/A",
    "PX14A6G": "PX14A6G",
    "CORRESP": "CORRESP",
    "UPLOAD": "UPLOAD",
    "SD": "SD",
    "ARS": "ARS",
    "424B5": "424B5"
}

def resolve_form_filter(user_input: str) -> str:
    cleaned = user_input.replace(" ", "").replace("-", "").upper()
    if cleaned in VALID_FORMS:
        return VALID_FORMS[cleaned]
    raise ValueError(f"Unknown or unsupported form type: {user_input}")
