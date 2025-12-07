# fred-regression-project

This repository contains Python code for fetching economic time-series data from the Federal Reserve Economic Data (FRED) API and preparing it for later regression analysis. The project currently includes a functional FRED client, a simple project structure for expansion, and a pytest-based testing suite.

## Project Purpose

The goal of this project is to build a reproducible workflow that:

Retrieves FRED series programmatically using the FRED API.

Converts API responses into pandas objects for analysis.

Supports testing and modular development.

Serves as a foundation for future regression tools and analysis modules.

This project will grow to include automated regressions, transformations, and integrated data checks.

## Directory Structure
fred-regression-project/
├── src/
│   ├── fred_client.py        # Fetches FRED series through the API
│   ├── regressions.py        # Placeholder for future regression-related code
│   └── __init__.py           # Marks src as a package
│
├── tests/
│   └── test_fred_client.py   # Unit tests for the FRED client
│
├── .gitignore                # Ignore rules for caches, venvs, and build artifacts
├── .gitattributes            # Git settings for text handling
└── README.md                 # Project documentation

## Installation
Clone the repository
git clone https://github.com/Larsmukherjee/fred-regression-project.git
cd fred-regression-project

## Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # macOS/Linux
.venv\Scripts\activate             # Windows

## Install dependencies

If the project uses a requirements file:

pip install -r requirements.txt

## FRED API Key

You will need a FRED API key, available for free at:

https://fred.stlouisfed.org/

Create a .env file in the root directory containing:

FRED_API_KEY=your_api_key_here


The client automatically reads this environment variable when fetching data.

## Basic Usage Example
from src.fred_client import fetch_series

## Fetch the unemployment rate starting in 2000
series = fetch_series("UNRATE", start="2000-01-01")

print(series.head())


The returned object is a pandas Series indexed by observation date.

## Running Tests

Tests are written using pytest. Run them with:

pytest


Pytest cache directories and artifacts are ignored via .gitignore.

## Future Development

Planned additions include:

Regression utilities built using statsmodels.

Automated preprocessing (e.g., differencing, date alignment, merging multiple FRED series).

Error-handling improvements and custom exceptions.

Optional CLI tools for fetching and analyzing data from the terminal.

Local caching so large API calls do not need to be repeated.

## Contributing

Before contributing changes, please ensure:

Code includes type hints and clear docstrings.

Tests pass successfully.

New modules or functions include appropriate test coverage.
