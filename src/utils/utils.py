from datetime import date

from src.exceptions import DateRangeException


def check_date_range_or_raise(date_from: date, date_to: date) -> None:
    """raises DateRangeException if date_from >= date_to"""
    if date_from >= date_to:
        raise DateRangeException
