from __future__ import annotations
import argparse, sys, pandas as pd, time
from pathlib import Path
from .mapping import ids_to_ciks
from .fetch import harvest
from .fetch import resolve_form_filter
from .api import Submissions


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Fetch SEC submissions metadata.")
    p.add_argument("identifiers", nargs="*", help="Positional tickers/CIKs")
    p.add_argument("-i","--input", help="CSV file with identifiers (must have 'cik' or 'ticker' column)")
    p.add_argument("-t","--type", choices=("ticker","cik"), default="ticker",
                   help="Identifier type if using positional args (default ticker)")
    p.add_argument("--form", help="Filter for a single form type (e.g. 10-K)")
    p.add_argument("-o","--out", default="sec_meta.csv", help="Output CSV")
    p.add_argument("-c","--credentials", required=False,
                   metavar='"Name <email@example.com>"',
                   help="Contact info for SEC User-Agent (required if not using --name/--email)")
    p.add_argument("--name", help="Contact name for SEC User-Agent (alternative to --credentials)")
    p.add_argument("--email", help="Contact email for SEC User-Agent (alternative to --credentials)")
    p.add_argument("--year-from", type=int, help="Filter: only filings from this year (inclusive)")
    p.add_argument("--year-to", type=int, help="Filter: only filings up to this year (inclusive)")
    p.add_argument("--sleep", type=float, default=1.0, help="Delay between companies")
    return p.parse_args(argv)

def main(argv=None):
    args = parse_args(argv)
    # Determine input mode
    if args.input:
        csv_path = args.input
        if not Path(csv_path).exists():
            sys.exit(f"input file {csv_path} not found")
        identifiers = None
    else:
        csv_path = None
        identifiers = args.identifiers
    if not (csv_path or identifiers):
        sys.exit("no identifiers given")

    # User-Agent logic
    if args.name and args.email:
        name = args.name
        email = args.email
        credentials = ""
    elif args.credentials:
        name = email = None
        credentials = args.credentials
    else:
        sys.exit("Must provide either --credentials or both --name and --email")

    # Only pass one of cik/ticker if not using CSV
    kwargs = dict(
        csv_path=csv_path,
        form=args.form,
        credentials=credentials,
        name=name,
        email=email,
        year_from=args.year_from,
        year_to=args.year_to
    )
    if identifiers:
        # If identifiers are given, treat as CIK or ticker depending on --type
        if args.type == "cik":
            kwargs["cik"] = identifiers[0] if len(identifiers) == 1 else None
            if len(identifiers) > 1:
                # Write to temp CSV for batch mode
                import tempfile, csv as pycsv
                with tempfile.NamedTemporaryFile("w", newline="", delete=False, suffix=".csv") as tf:
                    writer = pycsv.writer(tf)
                    writer.writerow(["cik"])
                    for val in identifiers:
                        writer.writerow([val])
                    kwargs["csv_path"] = tf.name
        else:
            kwargs["ticker"] = identifiers[0] if len(identifiers) == 1 else None
            if len(identifiers) > 1:
                import tempfile, csv as pycsv
                with tempfile.NamedTemporaryFile("w", newline="", delete=False, suffix=".csv") as tf:
                    writer = pycsv.writer(tf)
                    writer.writerow(["ticker"])
                    for val in identifiers:
                        writer.writerow([val])
                    kwargs["csv_path"] = tf.name

    try:
        sub = Submissions(**kwargs)
        df = sub.to_dataframe()
    except Exception as e:
        sys.exit(str(e))

    if df.empty:
        sys.exit("nothing fetched")
    df.to_csv(args.out, index=False)
    print(f"Finished - wrote {args.out}")

if __name__ == "__main__":
    main()

