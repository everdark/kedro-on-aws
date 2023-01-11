from typing import Callable, List


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
