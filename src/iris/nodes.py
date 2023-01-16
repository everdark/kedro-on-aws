"""
This is a boilerplate pipeline
generated using Kedro 0.18.4
"""

import logging
from typing import Dict

from pyspark.sql import DataFrame

from .config_loader import parameters
from .hooks import test_hook_var
from .utils import repartition_by

logger = logging.getLogger(__name__)
_partition_cols = parameters["partitions"]["parsed"]


@repartition_by(_partition_cols)
def read_raw_data(data: DataFrame, parameters: Dict) -> DataFrame:
    """Splits data into features and targets training and test sets.

    Args:
        data: The raw data.
        parameters: Parameters defined in parameters.yml.

    Returns:
        A pyspark dataframe.

    """
    logger.info(f"parameters read as: {parameters}")
    logger.info(f"globals in hook: {test_hook_var}")
    return data


def dummy(data: DataFrame, parameters: Dict) -> DataFrame:
    logger.info("running a dummy node")
    logger.info(f"parameters read as: {parameters}")
    logger.info(f"globals in hook: {test_hook_var}")
    return data
