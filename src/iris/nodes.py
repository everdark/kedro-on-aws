import logging
from typing import Dict

from pyspark.sql import DataFrame

from . import hooks
from .config_loader import parameters
from .utils import repartition_by

logger = logging.getLogger(__name__)
logger.info(f"check var update from hook: {hooks.PARTITION_SCHEME}")  # not updated yet
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
    logger.info("[node] running a dummy node")
    logger.info(f"[node] parameters read in a node as: {parameters}")
    logger.info(
        f"[node] globals updated by hook: {hooks.PARTITION_SCHEME}"
    )  # now updated
    return data
