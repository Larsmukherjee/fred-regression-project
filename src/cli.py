# src/cli.py

from __future__ import annotations

from typing import List, Tuple, Optional
from datetime import datetime


def prompt_series_ids() -> Tuple[str, List[str]]:
    """
    Prompt the user for:
      - one dependent (Y) FRED series ID
      - one or more independent (X) FRED series IDs, comma-separated

    Returns:
      (y_id, x_ids)
    """
    # Dependent / Y
    while True:
        y_id = input("Enter dependent (Y) FRED series ID (e.g., UNRATE): ").strip()
        if y_id:
            break
        print("Dependent series ID cannot be empty. Please try again.")

    # Independent / X
    while True:
        raw_x = input(
            "Enter independent (X) FRED series IDs, comma-separated "
            "(e.g., GDPC1, CPIAUCSL): "
        )
        x_ids = [s.strip() for s in raw_x.split(",") if s.strip()]
        if x_ids:
            break
        print("You must enter at least one independent series ID. Please try again.")

    return y_id, x_ids


def _prompt_single_date(label: str) -> Optional[str]:
    """
    Helper to prompt for a single date.

    Prompts:
      - "Enter start date (YYYY-MM-DD) or leave blank for no start limit: "
      - "Enter end date (YYYY-MM-DD) or leave blank for no end limit: "

    Returns:
      - a string in YYYY-MM-DD format, or
      - None if the user leaves it blank.
    """
    while True:
        text = input(
            f"Enter {label} date (YYYY-MM-DD) or leave blank for no {label} limit: "
        ).strip()

        if not text:
            return None

        try:
            # Validate format; we just return the string if it's valid.
            datetime.strptime(text, "%Y-%m-%d")
            return text
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD or leave blank.")


def prompt_date_range() -> Tuple[Optional[str], Optional[str]]:
    """
    Prompt the user for an optional start and end date.

    Returns:
      (start_date, end_date), each a 'YYYY-MM-DD' string or None.
    """
    start = _prompt_single_date("start")
    end = _prompt_single_date("end")
    return start, end
