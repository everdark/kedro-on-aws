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
  - [E04. Partition PySpark DataFrame with `globals` and repartition decorator](#e04-partition-pyspark-dataframe-with-globals-and-repartition-decorator)
  - [Miscellaneous](#miscellaneous)
    - [Dymanic `globals` via `settings.py`](#dymanic-globals-via-settingspy)

## Pipelines

- `train_and_register_model`: Train a `scikit-learn` model based on the `iris` dataset and save it to SageMaker Model Registry along with an inference module
- `deploy_model`: Deploy a SageMaker model package prepared by the pipeline `train_and_register_model`
- `athena`: Run a pipeline using Athena query as custom data source

## Experiments

### [E01. Integration with SageMaker Model Registry and Batch Transform Job](./docs/integration_with_sagemaker.md)

### [E02. Custom Kedro Dataset based on Athena Query](./docs/custom_dataset_athena_query.md)

### [E03. Read Dataset from S3 with PySpark](./docs/pyspark_read_from_s3.md)

### [E04. Partition PySpark DataFrame with `globals` and repartition decorator](./docs/partition_pyspark_dataframe.md)

### Miscellaneous

#### Dymanic `globals` via `settings.py`

Change `globals` programmatically to achieve dynamic `filepath` in dataset I/O.
Note that this is still quite restricted since `settings.py` cannot be hooked.
