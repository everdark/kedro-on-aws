"""
This is a boilerplate pipeline
generated using Kedro 0.18.4
"""

import logging
from typing import Dict

from pyspark.sql import DataFrame

from config_loader import parameters
from utils import repartition_by

logger = logging.getLogger(__name__)
_partition_cols = parameters["partition"]["parsed"]


@repartition_by(_partition_cols)
def read_raw_data(data: DataFrame) -> DataFrame:
    """Splits data into features and targets training and test sets.

    Args:
        data: The raw data.
        parameters: Parameters defined in parameters.yml.

    Returns:
        A pyspark dataframe.

    """
    return data
