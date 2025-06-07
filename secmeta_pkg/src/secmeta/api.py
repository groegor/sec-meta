from pathlib import Path
import pandas as pd
import re
from .fetch import harvest, resolve_form_filter
from .mapping import ids_to_ciks

class Submissions:
    def __init__(self,
                 cik: str | None = None,
                 ticker: str | None = None,
                 csv_path: str | None = None,
                 form: str | None = None,
                 credentials: str = "",
                 name: str | None = None,
                 email: str | None = None,
                 year_from: int | None = None,
                 year_to: int | None = None):
        if not (cik or ticker or csv_path):
            raise ValueError("Must provide either a CIK, ticker, or csv_path")

        if email and name:
            self.ua = f"secmeta ({name} <{email}>)"
        elif credentials:
            self.ua = f"secmeta ({credentials})"
        else:
            raise ValueError("Must provide either credentials= or both name= and email=")

        self.form = resolve_form_filter(form) if form else None
        self.year_from = year_from
        self.year_to = year_to

        self.batch_mode = bool(csv_path)
        self._csv_path = csv_path
        self._cik_list = []

        if csv_path:
            self._cik_list = self._load_ciks_from_csv(csv_path)
        else:
            id_ = cik or ticker
            is_cik = bool(cik)
            self._cik_list = [
                id_.zfill(10) if is_cik else ids_to_ciks([id_], "ticker", self.ua)[0]
            ]

    def _load_ciks_from_csv(self, path: str) -> list[str]:
        df = pd.read_csv(path)
        cols = [c.lower().strip() for c in df.columns]
        if "cik" in cols:
            ids = df[df.columns[cols.index("cik")]].astype(str).tolist()
            return [c.zfill(10) for c in ids if c.strip()]
        elif "ticker" in cols:
            ids = df[df.columns[cols.index("ticker")]].astype(str).tolist()
            return ids_to_ciks(ids, "ticker", self.ua)
        else:
            raise ValueError("CSV must contain a 'cik' or 'ticker' column")

    def to_dataframe(self) -> pd.DataFrame:
        all_rows = []
        for cik in self._cik_list:
            rows = harvest(cik, self.ua, self.form)
            all_rows.extend(rows)

        df = pd.DataFrame(all_rows)

        # Filter by fiscal report year (reportDate)
        if self.year_from or self.year_to:
            df["reportDate"] = pd.to_datetime(df["reportDate"], errors="coerce")
            if self.year_from:
                df = df[df["reportDate"].dt.year >= self.year_from]
            if self.year_to:
                df = df[df["reportDate"].dt.year <= self.year_to]

        return df

    def to_csv(self, path: str):
        df = self.to_dataframe()
        df.to_csv(path, index=False)
        return path

