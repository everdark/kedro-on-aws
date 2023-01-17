import logging
import os
import time
import uuid
from typing import Any, Dict, List, NoReturn

import boto3
from kedro.io.core import AbstractDataSet, DataSetError
from pyspark.sql import DataFrame, SparkSession

logger = logging.getLogger(__name__)


class AthenaQueryDataSet(AbstractDataSet[None, DataFrame]):
    """Custom dataset powered by Athena.

    It loads data from a provided Athena CTAS/UNLOAD query with partitioning columns.
    The resulting parquet outputs are written to S3 and read back by spark as dataframe,

    It does not support save method so it is a read only data set.
    """

    def __init__(
        self,
        region: str,
        database: str,
        bucket: str,
        athena_path: str,
        query: str,
        partition_cols: List[str],
        unload: bool = True,
    ) -> None:
        """Creates a new instance of AthenaQueryDataSet.

        Args:
            region: The region of our athena database.
            database: The name of the athena database we would like to query from.
            bucket: The S3 bucket we want to save the outputs of our queries to.
            athena_path: S3 prefix to save Athena outputs.
            query: The query that we would like to run and get output from.
            partition_cols: List of column names for output partitioning.
            unload: Use UNLOAD instead of CTAS query?

        """
        self._name = self._random_name()
        self._region = region
        self._database = database
        self._bucket = bucket
        self._athena_path = athena_path
        self._query = query
        self._partition_cols = partition_cols
        self._unload = unload
        # output location is used for storing athena query metadata regardless of
        # whether the query is CTAS or UNLOAD
        # in the case of CTAS, it is also used to save the output files
        self._output_location = f"s3://{self._bucket}/{self._athena_path}"
        # if unload is true, the output files are located instead by the unload location
        self._unload_location = os.path.join(self._output_location, self._name)

    @staticmethod
    def _random_name(prefix: str = "temp_tbl_", n_char: int = 10) -> str:
        """Generate random string for destination table/path naming.

        Args:
            prefix: Prefix for the resulting name.
            n_char: Number of characters used from UUID4.

        Returns:
            A random string of lenfth n_char.

        """
        return prefix + uuid.uuid4().hex[:n_char]

    def athena_query(self, client) -> Dict:
        """Create an Athena CTAS/UNLOAD query and execute it async."""
        with_clause = f"""
            WITH (
                format = 'PARQUET',
                partitioned_by = ARRAY{str(self._partition_cols)}
            )
        """
        if self._unload:
            final_query = f"""
            UNLOAD (
                {self._query}
            )
            TO '{self._unload_location}'
            {with_clause}
            """
            mesg = f"Attempt to UNLOAD files to {self._unload_location} with Athena."
        else:
            final_query = f"""
            CREATE TABLE {self._name}
            {with_clause}
            AS
            {self._query}
            """
            mesg = f"Attempt to create external table {self._name} with Athena CTAS."

        response = client.start_query_execution(
            QueryString=final_query,
            QueryExecutionContext={"Database": self._database},
            ResultConfiguration={"OutputLocation": self._output_location},
        )
        logger.info(mesg)

        return response

    def athena_to_s3(self) -> str:
        session = boto3.Session()
        client = session.client("athena", region_name=self._region)

        execution = self.athena_query(client)
        execution_id = execution["QueryExecutionId"]

        state = "RUNNING"
        while state in ["RUNNING", "QUEUED"]:
            response = client.get_query_execution(QueryExecutionId=execution_id)

            if (
                "QueryExecution" in response
                and "Status" in response["QueryExecution"]
                and "State" in response["QueryExecution"]["Status"]
            ):
                state = response["QueryExecution"]["Status"]["State"]
                if state == "FAILED":
                    raise DataSetError(
                        response["QueryExecution"]["Status"]["StateChangeReason"]
                    )
                elif state == "SUCCEEDED":
                    if self._unload:
                        s3_path = self._unload_location
                    else:
                        s3_path = response["QueryExecution"]["ResultConfiguration"][
                            "OutputLocation"
                        ]
                    logger.info(f"Athena query output files saved to: {s3_path}")
                    return s3_path.replace("s3://", "s3a://")

            time.sleep(1)

        return False

    def read_output_from_s3(self, s3a_path) -> DataFrame:
        spark = self._get_spark()
        logger.info("spark conf in use:")
        logger.info(spark.sparkContext.getConf().getAll())
        df = spark.read.parquet(s3a_path)
        return df

    @staticmethod
    def _get_spark():
        return SparkSession.builder.getOrCreate()

    def _load(self) -> DataFrame:
        """Loads data from the image file.

        Returns:
            Data from the image file as a numpy array.
        """
        s3_filename = self.athena_to_s3()
        return self.read_output_from_s3(s3_filename)

    def _describe(self) -> Dict[str, Any]:
        return {
            "region": self._region,
            "database": self._database,
            "bucket": self._bucket,
            "athena_path": self._athena_path,
            "query": self._query,
        }

    def _save(self, data: None) -> NoReturn:
        raise DataSetError("'save' is not supported on AthenaQueryDataSet")
