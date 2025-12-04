import streamlit as st
import pandas as pd

from src.fred_client import fetch_series
from src.regression import run_ols
from src.plotting import plot_actual_vs_fitted
from src.variable_options import VARIABLE_OPTIONS

st.set_page_config(page_title="FRED Regression Dashboard", layout="wide")

st.title("📊 FRED Regression Dashboard")

st.write(
    "Select variables below to run an OLS regression using data pulled live from the Federal Reserve (FRED)."
)

# --- User selections ---
y_label = st.selectbox("Select dependent variable (Y):", list(VARIABLE_OPTIONS.keys()))

x_labels = st.multiselect(
    "Select independent variables (X):",
    list(VARIABLE_OPTIONS.keys()),
)

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

    y_id = VARIABLE_OPTIONS[y_label]
    x_ids = [VARIABLE_OPTIONS[x] for x in x_labels]

    with st.spinner("Fetching data from FRED..."):
        try:
            y = fetch_series(y_id, start=start, end=end)
            X_dict = {label: fetch_series(fid, start=start, end=end) for label, fid in zip(x_labels, x_ids)}
        except ValueError as e:
            st.error(f"Data fetch failed: {e}")
            st.stop()

    X_df = pd.concat(X_dict.values(), axis=1)
    X_df.columns = X_dict.keys()

    with st.spinner("Running regression..."):
        try:
            result = run_ols(y, X_df)
        except ValueError as e:
            st.error(f"Regression failed: {e}")
            st.stop()

    r2 = result["r_squared"]
    model = result["model"]

    st.success(f"### R² = **{r2:.4f}**")

    # Show coefficients
    st.write("### Coefficients")
    st.dataframe(model.params.rename("Coefficient"))

    # Plot
    fitted = model.fittedvalues
    y_aligned = y.loc[fitted.index]

    fig = plot_actual_vs_fitted(
        y_aligned,
        fitted,
        title=f"Actual vs Fitted: {y_label}",
        return_fig=True,
    )

    st.write("### Actual vs Fitted Plot")
    st.pyplot(fig)
