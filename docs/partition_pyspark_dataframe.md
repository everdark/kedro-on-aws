# E04. Partition PySpark DataFrame with `globals` and repartition decorator

All resulting datasets are `pyspark` dataframe.
We'd like to persist them as partitioned parquet files on S3.
We use `globals` as the single source of truth for partitioning scheme,
with the help of yaml templating to configure the built-in kedro `SparkDataSet`.

We also use a [repartition decorator](../src/iris/utils.py) to control how data are distributed across partitions.

By design, parameters in general cannot be accessed outside the node function.
It is possible to use hooks to populate it to Python globals and access it within, say, a pipeline function.
But as a general constants across the module this update is not timely.
A [`config_loader.py`](../src/iris/config_loader.py) module is introduced to workaround this issue.
