# src/transforms.py

from __future__ import annotations

import numpy as np
import pandas as pd


TRANSFORM_CHOICES = [
    "Level",
    "Growth rate (% change)",
    "Year-on-year % change",
]


def apply_transform(series: pd.Series, choice: str) -> pd.Series:
    """
    Apply a transformation to a time series.

    - "Level": raw series
    - "Growth rate (% change)": 100 * (s_t - s_{t-1}) / s_{t-1}
    - "Year-on-year % change": 100 * (s_t - s_{t-12}) / s_{t-12}

    NaNs introduced by differencing are left in; run_ols will drop them.
    """
    if choice == "Level":
        return series

    if choice == "Growth rate (% change)":
        return series.pct_change(periods=1) * 100.0

    if choice == "Year-on-year % change":
        return series.pct_change(periods=12) * 100.0

    # Fallback: no transform
    return series
