import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

import streamlit as st
import pandas as pd

from src.fred_client import fetch_series
from src.regression import run_ols
from src.plotting import plot_scatter_with_fit
from src.variable_options import VARIABLES
from src.transforms import TRANSFORM_CHOICES, apply_transform

st.set_page_config(page_title="FRED Regression Dashboard", layout="wide")
st.title("📊 FRED Regression Dashboard")
st.write(
    "Run regressions on basic macro variables (unemployment, money, prices, GDP) "
    "using levels, growth rates, or year-on-year changes."
)

mode = st.radio(
    "Mode:",
    ["Custom regression", "Phillips Curve (inflation vs unemployment)"],
)

var_names = list(VARIABLES.keys())

if mode == "Custom regression":
    # --- Custom regression UI ---
    y_label = st.selectbox("Select dependent variable (Y):", var_names)

    y_transform_choice = st.selectbox(
        "Transform for Y:",
        TRANSFORM_CHOICES,
        index=1,  # default: growth rate
    )

    x_labels = st.multiselect(
        "Select independent variables (X):",
        var_names,
    )

    x_transform_choice = st.selectbox(
        "Transform for all X variables:",
        TRANSFORM_CHOICES,
        index=1,
    )

else:
    # --- Phillips Curve preset ---
    st.markdown("**Phillips Curve:** inflation (YoY CPI) vs unemployment rate.")
    y_label = "Unemployment rate (UNRATE)"
    x_labels = ["Price level: CPI (CPIAUCSL)"]
    # For Phillips Curve:
    #   Y = inflation (YoY % change from CPI) -> so transform CPI
    #   X = unemployment rate in level
    y_transform_choice = "Year-on-year % change"
    x_transform_choice = "Level"

start_date = st.date_input("Start date (optional):", value=None)
end_date = st.date_input("End date (optional):", value=None)

start = str(start_date) if start_date else None
end = str(end_date) if end_date else None

run_button = st.button("Run Regression")
# --- Logic ---
if run_button:
    if not x_labels:
        st.error("Please choose at least one independent variable.")
        st.stop()

    # Map labels to FRED IDs
    y_meta = VARIABLES[y_label]
    y_id = y_meta["id"]

    x_meta_list = [VARIABLES[name] for name in x_labels]
    x_ids = [m["id"] for m in x_meta_list]

    with st.spinner("Fetching data from FRED..."):
        try:
            y_level = fetch_series(y_id, start=start, end=end)
            X_level_dict = {
                label: fetch_series(mid["id"], start=start, end=end)
                for label, mid in zip(x_labels, x_meta_list)
            }
        except ValueError as e:
            st.error(f"Data fetch failed: {e}")
            st.stop()

    # Apply transforms
    if mode == "Custom regression":
        y_trans = apply_transform(y_level, y_transform_choice)
        X_trans_dict = {
            label: apply_transform(series, x_transform_choice)
            for label, series in X_level_dict.items()
        }
    else:
        # Phillips Curve:
        #   inflation_t (YoY from CPI) as Y
        #   unemployment rate (level) as X
        # Here y_level is unemployment, X_level_dict has CPI
        # We want Y = inflation, X = unemployment
        cpi_series = list(X_level_dict.values())[0]
        infl = apply_transform(cpi_series, "Year-on-year % change")
        y_trans = infl
        X_trans_dict = {"Unemployment rate (UNRATE)": y_level}
        x_labels = ["Unemployment rate (UNRATE)"]  # rename for display

    X_df = pd.concat(X_trans_dict.values(), axis=1)
    X_df.columns = X_trans_dict.keys()

    with st.spinner("Running regression..."):
        try:
            result = run_ols(y_trans, X_df)
        except ValueError as e:
            st.error(f"Regression failed: {e}")
            st.stop()

    r2 = result["r_squared"]
    model = result["model"]

    st.success(f"### R² = **{r2:.4f}**")

    st.write("### Coefficients")
    st.dataframe(model.params.rename("Coefficient"))

    # Scatter plot only when one X
    fitted = model.fittedvalues
    y_aligned = y_trans.loc[fitted.index]

    if len(X_df.columns) == 1:
        x_name = list(X_df.columns)[0]
        x_series = X_df[x_name].loc[fitted.index]
        fig = plot_scatter_with_fit(
            y_aligned,
            x_series,
            fitted,
            title=f"{y_label} ({y_transform_choice}) vs {x_name} ({x_transform_choice})"
            if mode == "Custom regression"
            else "Phillips Curve: inflation (YoY CPI) vs unemployment",
            return_fig=True,
        )
        st.write("### Scatter plot with regression line")
        st.pyplot(fig)
    else:
        st.info("Scatter plot only shown when exactly one independent variable is selected.")