# src/main.py

from __future__ import annotations

from typing import List, Dict

import pandas as pd

from src.fred_client import fetch_series
from src.regression import run_ols


def fetch_X_dataframe(x_ids: List[str]) -> pd.DataFrame:
    """
    Fetch multiple FRED series into a single DataFrame with columns
    named by their series IDs.
    """
    series_dict: Dict[str, pd.Series] = {}

    for series_id in x_ids:
        s = fetch_series(series_id)
        series_dict[series_id] = s

    # Align via index when concatenating; columns are series IDs
    X = pd.concat(series_dict.values(), axis=1, keys=series_dict.keys())
    return X


def main() -> None:
    # Hard-coded for Milestone 2
    y_id = "UNRATE"
    x_ids = ["GDPC1"]

    # Fetch Y and X series
    y = fetch_series(y_id)
    X = fetch_X_dataframe(x_ids)

    # Run regression (run_ols will handle index alignment and NaNs)
    result = run_ols(y, X)

    r2 = result["r_squared"]
    print(f"R² for {y_id} ~ {', '.join(x_ids)}: {r2:.4f}")


if __name__ == "__main__":
    main()