# src/plotting.py

from __future__ import annotations

from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt


def plot_actual_vs_fitted(
    y: pd.Series,
    fitted: pd.Series,
    title: str = "Actual vs Fitted",
    return_fig: bool = False,
):
    """
    Plot actual vs fitted values over time using matplotlib.

    Assumes the indices of y and fitted are already aligned.
    If return_fig=True, returns the figure object for use in Streamlit.
    Otherwise, calls plt.show().
    """

    fig, ax = plt.subplots()

    ax.plot(y.index, y.values, label="Actual")
    ax.plot(fitted.index, fitted.values, label="Fitted", linestyle="--")

    ax.set_xlabel("Time")
    ax.set_ylabel(y.name or "Value")
    ax.set_title(title)
    ax.legend()
    fig.autofmt_xdate()
    plt.tight_layout()

    if return_fig:
        return fig

    plt.show()