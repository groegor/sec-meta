# SEC Meta

A Python package for fetching SEC EDGAR filings data for companies by ticker symbol or CIK number.

[![PyPI version](https://img.shields.io/pypi/v/secmeta.svg)](https://pypi.org/project/secmeta/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

SEC Meta provides a simple and efficient way to retrieve SEC filing data from the EDGAR database. It supports searching by:

- Company ticker symbols (e.g., AAPL, MSFT)
- CIK numbers
- Lists of companies from CSV files

## Features

- **Multiple Search Options**: Search by ticker, CIK, or CSV file containing multiple companies
- **Form Filtering**: Filter by specific filing types (10-K, 10-Q, 8-K, etc.)
- **Date Range**: Limit results to specific years
- **Command Line Interface**: Use directly from the terminal
- **Python API**: Integrate into your Python scripts and applications
- **SEC Compliant**: Built-in user-agent handling for SEC API requirements

## Installation

Install from PyPI:

```bash
pip install secmeta
```

## Usage

### Command Line Interface

```bash
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

```python
from secmeta import Submissions

# Get filings by CIK
df_cik = Submissions(
    cik="0001288776",  # Google's CIK
    form="10-K", 
    name="John Doe", 
    email="example@email.com"
).to_dataframe()

# Get filings by ticker
df_ticker = Submissions(
    ticker="GOOGL", 
    form="10-K", 
    name="John Doe", 
    email="example@email.com"
).to_dataframe()

# Get filings from a CSV file
df_csv = Submissions(
    csv_path="input_companies.csv", 
    form="10-K", 
    name="John Doe", 
    email="example@email.com"
).to_dataframe()
```

## CSV Input Format

For the `-i` option or `csv_path` parameter, your CSV file should contain company identifiers:

```csv
cik
0001288776
0000320193
```

or

```csv
ticker
AAPL
GOOGL
```

## Requirements

- Python 3.8+
- pandas
- requests

## SEC API Requirements

The SEC requires all EDGAR API users to identify themselves with a user-agent string including a name and email. You can provide this with:

```bash
# As credentials parameter
secmeta AAPL -c "Your Name <your@email.com>"

# Or as separate name and email
secmeta AAPL --name "Your Name" --email "your@email.com"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is not affiliated with the U.S. Securities and Exchange Commission (SEC). When using this tool, please respect the [SEC's fair access policy](https://www.sec.gov/os/accessing-edgar-data).
