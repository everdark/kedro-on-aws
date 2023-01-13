import datetime
from typing import Callable, List

import pytz


def today(tzname: str = "Asia/Singapore") -> datetime.date:
    """Get datetime for today at a given timezone.

    Args:
        tzname: A timezone name, e.g., Asia/Singapore.

    Returns:
        A datetime.date.

    """
    tz = pytz.timezone(tzname)
    now = datetime.datetime.now(tz)
    today = now.date()
    return today


def yesterday(tzname: str = "Asia/Singapore") -> datetime.date:
    """Get datetime for yesterday at a given timezone.

    Args:
        tzname: A timezone name, e.g., Asia/Singapore.

    Returns:
        A datetime.date.

    """
    return today() - datetime.timedelta(days=1)


def repartition_by(cols: List[str]) -> Callable:
    """A decorator to repartition a function's pyspark dataframe before return.

    Args:
        cols: List of column names for repartitioning.

    Returns:
        The decorated function.

    """

    def decorator(function: Callable):
        def wrapper(*args, **kwargs):
            df = function(*args, **kwargs)
            return df.repartition(*cols)

        return wrapper

    return decorator
