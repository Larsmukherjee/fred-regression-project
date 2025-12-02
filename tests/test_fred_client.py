import pandas as pd
import pytest

from src.fred_client import fetch_series


def test_fetch_series_returns_series_with_datetime_index():
    series = fetch_series("UNRATE", "2010-01-01", "2011-01-01")

    assert isinstance(series, pd.Series)
    assert not series.empty
    assert isinstance(series.index, pd.DatetimeIndex)


def test_fetch_series_invalid_id_raises_value_error():
    with pytest.raises(ValueError):
        fetch_series("THIS_IS_NOT_A_REAL_SERIES")
