# kedro-on-aws

## Experiments

- Using a custom kedro dataset with Athena query

In case the raw data is challenging to parse (e.g., unfriendly partitioned),
we can introduce an Athena query layer to serve as the actual entrypoint to the raw data.
We can use CTAS or UNLOAD queries to make sure the resulting files are properly partitioned for the downstream pipeline.

- Read parameters outside node functions

Parameters in general cannot be accessed outside the node function.
It is possible to use hooks to populate it to Python globals and access it within, say, a pipeline function.
But as a general constants across the module this update is not timely.
A `config_loader.py` module is introduced to workaround this issue.

The use case is for a decorator to depends on parameters as its argument to decorate node functions.

- PySpark DataFrame partitioning with `globals` configuration and repartition decorator

All resulting datasets are pyspark dataframe.
We'd like to persist them as partitioned parquet files on S3.
We use `globals` as the single source of truth for partitioning scheme,
with the help of yaml templating to configure the built-in kedro `SparkDataSet`.

We also use a repartition decorator to control how data are distributed across partitions.

- Dymanic `globals` in `settings.py`

Change `globals` programmatically to achieve dynamic `filepath` in dataset I/O.
This is still quite restricted since `settings.py` cannot be hooked.

## Data

- [AWS Public Blockchain Data](https://aws.amazon.com/marketplace/pp/prodview-xv4ehzlgtim5a)

Schema can be found here:
- https://github.com/aws-samples/digital-assets-examples/blob/main/analytics/consumer/schema/eth.md

```bash
aws s3 ls aws-public-blockchain/v1.0/eth/transactions/
```

## Prep

```bash
pip install -r src/requirements.txt
```

To allow `pyspark` to read files from `s3`, we will need two jars:

- [hadoop-aws](https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws)
- [aws-java-sdk-bundle](https://mvnrepository.com/artifact/com.amazonaws/aws-java-sdk-bundle)

The kedro template used in this repo is simply created by:

```bash
kedro new --starter=pyspark-iris
```

We use [Terraform](https://www.terraform.io/) to manage the required AWS resources.

### AWS S3

We need a bucket to locate Athena query outputs.
We can also copy some files from the public dataset to our own bucket for experiments.

Refer to `./terraform` for details.

### AWS Glue

We need a Glue database and table for Athena to query the files on S3.

Refer to `./terraform` for details.
