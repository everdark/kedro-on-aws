# kedro-on-aws

The repository is a playground for experiments about using [Kedro](https://github.com/kedro-org/kedro) on AWS.

The project is bootstrapepd from the `pyspark-iris` starter template:

```bash
kedro new --starter=pyspark-iris
```

To install the dependencies:

```bash
pip install -r src/requirements.txt
```

- [Pipelines](#pipelines)
- [Experiments](#experiments)
  - [E01. Integration with SageMaker Model Registry and Batch Transform Job](#e01-integration-with-sagemaker-model-registry-and-batch-transform-job)
  - [E02. Custom Kedro Dataset based on Athena Query](#e02-custom-kedro-dataset-based-on-athena-query)
  - [E03. Read Dataset from S3 with PySpark](#e03-read-dataset-from-s3-with-pyspark)
  - [Read parameters outside node functions](#read-parameters-outside-node-functions)
  - [PySpark DataFrame partitioning with `globals` configuration and repartition decorator](#pyspark-dataframe-partitioning-with-globals-configuration-and-repartition-decorator)
  - [Dymanic `globals` in `settings.py`](#dymanic-globals-in-settingspy)

## Pipelines

- `train_and_register_model`: Train a `scikit-learn` model based on the `iris` dataset and save it to SageMaker Model Registry along with an inference module
- `deploy_model`: Deploy a SageMaker model package prepared by the pipeline `train_and_register_model`
- `athena`: Run a pipeline using Athena query as custom data source

## Experiments

### [E01. Integration with SageMaker Model Registry and Batch Transform Job](./docs/integration_with_sagemaker.md)

### [E02. Custom Kedro Dataset based on Athena Query](./docs/custom_dataset_athena_query.md)

### [E03. Read Dataset from S3 with PySpark](./docs/pyspark_read_from_s3.md)

### Read parameters outside node functions

Parameters in general cannot be accessed outside the node function.
It is possible to use hooks to populate it to Python globals and access it within, say, a pipeline function.
But as a general constants across the module this update is not timely.
A `config_loader.py` module is introduced to workaround this issue.

The use case is for a decorator to depends on parameters as its argument to decorate node functions.

### PySpark DataFrame partitioning with `globals` configuration and repartition decorator

All resulting datasets are pyspark dataframe.
We'd like to persist them as partitioned parquet files on S3.
We use `globals` as the single source of truth for partitioning scheme,
with the help of yaml templating to configure the built-in kedro `SparkDataSet`.

We also use a repartition decorator to control how data are distributed across partitions.

### Dymanic `globals` in `settings.py`

Change `globals` programmatically to achieve dynamic `filepath` in dataset I/O.
This is still quite restricted since `settings.py` cannot be hooked.
