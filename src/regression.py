# src/regression.py

from __future__ import annotations

from typing import Any, Dict

import pandas as pd
import statsmodels.api as sm


def run_ols(y: pd.Series, X: pd.DataFrame) -> Dict[str, Any]:
    """
    Run an OLS regression of y on X with an intercept.

    - Aligns y and X on the intersection of their indices.
    - Drops any rows with missing values.
    - Fits the model using statsmodels.
    - Returns a dict with at least:
        {
            "r_squared": float,
            "model": fitted_model
        }
    """
    if not isinstance(X, pd.DataFrame):
        raise TypeError("X must be a pandas DataFrame.")

    # Combine y and X, align on common index, and drop missing values
    combined = pd.concat([y, X], axis=1, join="inner").dropna()

    if combined.empty:
        raise ValueError("No overlapping, non-missing observations between y and X.")

    # First column is y, remaining columns are X
    y_aligned = combined.iloc[:, 0]
    X_aligned = combined.iloc[:, 1:]

    # Add intercept
    X_with_const = sm.add_constant(X_aligned, has_constant="add")

    model = sm.OLS(y_aligned, X_with_const)
    results = model.fit()

    return {
        "r_squared": float(results.rsquared),
        "model": results,
    }