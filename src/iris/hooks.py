import logging
from typing import Any, Dict

from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog
from pyspark import SparkConf
from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)
PARTITION_SCHEME: Dict = {}


class ContextHooks:
    @hook_impl
    def after_context_created(self, context) -> None:
        """Update global variables from params to be accessible outside nodes."""
        logger.info(f"[context hook] params read: {context.params}")

        global PARTITION_SCHEME
        PARTITION_SCHEME = context.params["partitions"]


class CatalogHooks:
    @hook_impl
    def after_catalog_created(
        self,
        catalog: DataCatalog,
        conf_catalog: Dict[str, Any],
        conf_creds: Dict[str, Any],
        save_version: str,
        load_versions: Dict[str, str],
    ) -> None:
        """Dummy hook on catalog."""
        logger.info(f"[catalog hook] conf read: {conf_catalog}")


class SparkHooks:
    @hook_impl
    def after_context_created(self, context) -> None:
        """Initialises a SparkSession using the config
        defined in project's conf folder.
        """
        # Load the spark configuration in spark.yaml using the config loader
        parameters = context.config_loader.get("spark*", "spark*/**")
        spark_conf = SparkConf().setAll(parameters.items())

        # Initialise the spark session
        spark_session_conf = (
            SparkSession.builder.appName(context._package_name)
            .master("local[2]")  # minimum parallelism
            .enableHiveSupport()
            .config(conf=spark_conf)
        )
        _spark_session = spark_session_conf.getOrCreate()
        _spark_session.sparkContext.setLogLevel("WARN")
