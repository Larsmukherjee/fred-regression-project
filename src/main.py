# src/main.py

from __future__ import annotations

from typing import List, Dict, Optional

import pandas as pd

from src.cli import prompt_series_ids, prompt_date_range
from src.fred_client import fetch_series
from src.regression import run_ols
from src.plotting import plot_actual_vs_fitted  # NEW import


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
        s = fetch_series(series_id, start=start, end=end)
        series_dict[series_id] = s

    if not series_dict:
        raise ValueError("No independent series to fetch.")

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
        print(f"Error running regression: {e}")
        return

    r2 = result["r_squared"]
    model = result["model"]

    print()
    print("===================================================")
    print(f"R² for {y_id} ~ {', '.join(x_ids)}: {r2:.4f}")
    print("===================================================")

    # 5. Optionally show plot of actual vs fitted
    answer = input("Show plot of actual vs fitted values? (y/n): ").strip().lower()
    if answer.startswith("y"):
        # model.fittedvalues has index equal to the aligned y used in regression
        fitted = model.fittedvalues

        # Align original y to the fitted index (just to be safe)
        y_aligned = y.loc[fitted.index]

        title = f"Actual vs Fitted: {y_id} ~ {', '.join(x_ids)}"
        plot_actual_vs_fitted(y_aligned, fitted, title=title)


if __name__ == "__main__":
    main()