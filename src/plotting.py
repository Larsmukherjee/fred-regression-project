# src/plotting.py

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_scatter_with_fit(y: pd.Series, x: pd.Series, fitted: pd.Series, title="Scatter Plot with Regression Line", return_fig=False):
    fig, ax = plt.subplots()

    # Scatter plot of data points
    ax.scatter(x, y, alpha=0.6, label="Data Points")

    # Regression line
    sorted_idx = np.argsort(x)
    ax.plot(x.iloc[sorted_idx], fitted.iloc[sorted_idx], color="red", label="Regression Line")

    ax.set_xlabel(x.name or "X")
    ax.set_ylabel(y.name or "Y")
    ax.set_title(title)
    ax.legend()

    if return_fig:
        return fig

    plt.show()
