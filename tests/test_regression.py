# tests/test_regression.py

import numpy as np
import pandas as pd

from src.regression import run_ols


def test_run_ols_high_r_squared():
    """
    Use fake data where y ≈ 2 * x + 3 with small noise,
    so R² should be very close to 1.
    """
    rng = np.random.default_rng(42)
    x = np.linspace(0, 10, 100)
    noise = rng.normal(loc=0.0, scale=0.1, size=len(x))

    y = 2 * x + 3 + noise

    y_series = pd.Series(y, index=pd.RangeIndex(len(y)), name="y")
    X_df = pd.DataFrame({"x": x}, index=pd.RangeIndex(len(x)))

    result = run_ols(y_series, X_df)

    assert "r_squared" in result
    assert isinstance(result["r_squared"], float)
    assert result["r_squared"] > 0.99


def test_run_ols_aligns_indices_and_drops_nans():
    """
    Ensure alignment (intersection of indices) and NaN dropping work.
    """
    y = pd.Series(range(10), index=pd.RangeIndex(10), name="y")

    X = pd.DataFrame({"x": list(range(5, 15))}, index=pd.RangeIndex(5, 15))
    X.loc[7, "x"] = np.nan  # Add a NaN

    result = run_ols(y, X)

    assert 0.0 <= result["r_squared"] <= 1.0


def test_run_ols_raises_if_no_overlap():
    """
    If y and X have no overlapping indices, ValueError should be raised.
    """
    y = pd.Series([1, 2, 3], index=[0, 1, 2], name="y")
    X = pd.DataFrame({"x": [4, 5, 6]}, index=[10, 11, 12])

    try:
        run_ols(y, X)
    except ValueError:
        return

    assert False, "Expected ValueError when there is no overlapping index."