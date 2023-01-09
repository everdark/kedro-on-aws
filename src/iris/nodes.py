"""
This is a boilerplate pipeline
generated using Kedro 0.18.4
"""

import logging
from typing import Dict

from pyspark.sql import DataFrame

logger = logging.getLogger(__name__)


def read_raw_data(data: DataFrame, parameters: Dict):
    """Splits data into features and targets training and test sets.

    Args:
        data: The raw data.
        parameters: Parameters defined in parameters.yml.

    Returns:
        ...

    """
    return data
