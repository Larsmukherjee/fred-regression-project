import requests
import pandas as pd
from typing import Optional

from src.config import get_fred_api_key

FRED_SERIES_URL = "https://api.stlouisfed.org/fred/series/observations"


def _build_params(series_id: str, start: Optional[str], end: Optional[str]) -> dict:
    params = {
        "series_id": series_id,
        "api_key": get_fred_api_key(),
        "file_type": "json",
    }
    if start:
        params["observation_start"] = start
    if end:
        params["observation_end"] = end
    return params


def _parse_observations(data: dict, series_id: str) -> pd.Series:
    if "error_message" in data:
        raise ValueError(f"FRED API error for series '{series_id}': {data['error_message']}")

    observations = data.get("observations")
    if not isinstance(observations, list):
        raise ValueError(f"Unexpected response structure for series '{series_id}': missing observations.")

    dates = []
    values = []
    for obs in observations:
        date = obs.get("date")
        value = obs.get("value")
        if date is None or value is None:
            raise ValueError(f"Missing date or value in observation for series '{series_id}'.")
        dates.append(date)
        values.append(value)

    try:
        index = pd.to_datetime(dates, format="%Y-%m-%d", errors="raise")
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid date format in observations for series '{series_id}'.") from exc

    numeric_values = pd.to_numeric(values, errors="coerce")
    return pd.Series(numeric_values, index=index, name=series_id)


def fetch_series(series_id: str, start: Optional[str] = None, end: Optional[str] = None) -> pd.Series:
    params = _build_params(series_id, start, end)
    try:
        response = requests.get(FRED_SERIES_URL, params=params, timeout=10)
    except requests.RequestException as exc:
        raise ValueError(f"Request failed for series '{series_id}': {exc}") from exc

    if response.status_code != 200:
        raise ValueError(f"FRED API request failed for series '{series_id}' with status code {response.status_code}.")

    try:
        data = response.json()
    except ValueError as exc:
        raise ValueError(f"Unable to parse JSON response for series '{series_id}'.") from exc

    return _parse_observations(data, series_id)
