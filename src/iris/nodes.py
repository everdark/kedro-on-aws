import logging
from typing import Dict

from pyspark.sql import DataFrame

from . import hooks
from .config_loader import parameters
from .utils import repartition_by

logger = logging.getLogger(__name__)
logger.info(f"check hooked var: {hooks.PARTITION_SCHEME}")  # not updated yet
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
    return data


def dummy(data: DataFrame, parameters: Dict) -> DataFrame:
    logger.info("running a dummy node")
    logger.info(f"parameters read in a node as: {parameters}")
    logger.info(f"globals in a node updated by hook: {hooks.PARTITION_SCHEME}")  # now updated
    return data
