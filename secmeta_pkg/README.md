# SEC Meta

A Python package for fetching SEC filings data for companies by ticker or CIK.

## Installation

```bash
pip install secmeta
```

## Usage
### Command Line Interface
```
# Get filings for a ticker
secmeta AAPL -c "Your Name <your@email.com>"

# Get filings for multiple tickers
secmeta AAPL MSFT GOOGL -c "Your Name <your@email.com>"

# Get filings from a CSV file
secmeta -i companies.csv -c "Your Name <your@email.com>"

# Filter by form type and date range
secmeta AAPL --form 10-K --year-from 2020 --year-to 2025 -c "Your Name <your@email.com>"

```

### Python API 
```
from secmeta import Submissions

# Get filings by CIK
df_cik = Submissions(cik="0001288776", form="10-K", name="John Doe", email="example@email.com").to_dataframe()

# Get filings by ticker
df_ticker = Submissions(ticker="GOOGL", form="10-K", name="John Doe", email="example@email.com").to_dataframe()

# Get filings from a CSV file
df_csv = Submissions(csv_path="input_companies.csv", form="10-K", name="John Doe", email="example@email.com").to_dataframe()
```
