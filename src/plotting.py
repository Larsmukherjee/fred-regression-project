# src/plotting.py

from __future__ import annotations

from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt


def plot_actual_vs_fitted(
    y: pd.Series,
    fitted: pd.Series,
    title: str = "Actual vs Fitted",
    y_label: Optional[str] = None,
) -> None:
    """
    Plot actual vs fitted values over time using matplotlib.

    Assumes that indices of y and fitted are already aligned.
    """
    if y_label is None:
        y_label = y.name or "Value"

    fig, ax = plt.subplots()

    ax.plot(y.index, y.values, label="Actual")
    ax.plot(fitted.index, fitted.values, label="Fitted", linestyle="--")

    ax.set_xlabel("Time")
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    fig.autofmt_xdate()  # nicer date labels
    plt.tight_layout()
    plt.show()
