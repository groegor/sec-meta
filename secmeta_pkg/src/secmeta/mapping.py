from __future__ import annotations
import json, requests, sys
from pathlib import Path
from typing import Iterable, List

MAP_URL = "https://www.sec.gov/files/company_tickers.json"

def _load_map(user_agent: str) -> dict:
    cache = Path.home() / ".sec_company_tickers.json"
    if cache.exists():
        return json.loads(cache.read_text())
    print("[info] downloading ticker map …", file=sys.stderr)
    r = requests.get(MAP_URL, headers={"User-Agent": user_agent}, timeout=30)
    r.raise_for_status()
    data = r.json()
    cache.write_text(json.dumps(data))
    return data

def ids_to_ciks(ids: Iterable[str], id_type: str, user_agent: str) -> List[str]:
    if id_type == "cik":
        return [x.zfill(10) for x in ids if x.strip()]
    mapping = _load_map(user_agent)
    out: List[str] = []
    for ident in ids:
        ident = ident.strip()
        if not ident:
            continue
        match = next((v for v in mapping.values() if v["ticker"].casefold() == ident.casefold()), None)
        if match:
            out.append(str(match["cik_str"]).zfill(10))
        else:
            print(f"[warn] no CIK for ticker {ident}", file=sys.stderr)
    return out
