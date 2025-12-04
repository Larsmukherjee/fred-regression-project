# src/main.py

from __future__ import annotations

from typing import List, Dict, Optional

import pandas as pd

from src.cli import prompt_series_ids, prompt_date_range
from src.fred_client import fetch_series
from src.regression import run_ols


def fetch_X_dataframe(
    x_ids: List[str],
    start: Optional[str] = None,
    end: Optional[str] = None,
) -> pd.DataFrame:
    """
    Fetch multiple FRED series into a single DataFrame with columns
    named by their series IDs.

    Raises:
        ValueError if any of the series fail to fetch.
    """
    series_dict: Dict[str, pd.Series] = {}

    for series_id in x_ids:
        # Let fetch_series raise ValueError for invalid IDs or request issues.
        s = fetch_series(series_id, start=start, end=end)
        series_dict[series_id] = s

    if not series_dict:
        raise ValueError("No independent series to fetch.")

    # Align via index when concatenating; columns are series IDs
    X = pd.concat(series_dict.values(), axis=1, keys=series_dict.keys())
    return X


def main() -> None:
    # 1. Prompt the user for series IDs and date range
    y_id, x_ids = prompt_series_ids()
    start, end = prompt_date_range()

    # 2. Fetch Y
    try:
        y = fetch_series(y_id, start=start, end=end)
    except ValueError as e:
        print(f"Error fetching dependent series '{y_id}': {e}")
        return

    # 3. Fetch X DataFrame
    try:
        X = fetch_X_dataframe(x_ids, start=start, end=end)
    except ValueError as e:
        print(f"Error fetching independent series: {e}")
        return

    # 4. Run regression
    try:
        result = run_ols(y, X)
    except ValueError as e:
        # e.g., no overlapping observations between series
        print(f"Error running regression: {e}")
        return

    # 5. Print R²
    r2 = result["r_squared"]
    print()
    print("===================================================")
    print(f"R² for {y_id} ~ {', '.join(x_ids)}: {r2:.4f}")
    print("===================================================")


if __name__ == "__main__":
    main()