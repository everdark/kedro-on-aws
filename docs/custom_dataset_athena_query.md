# E02. Custom Kedro Dataset based on Athena Query

Implement a custom dataset [AthenaQueryDataSet](../src/iris/extras/datasets/athena_dataset.py) to handle data source based on Athena query.
This is useful when the source data files are not user-friendly for loading.
For example, when the source data files are not properly partitioned.

We can use either CTAS or UNLOAD queries to make sure the resulting files are properly partitioned for the downstream pipeline.

## Prerequisites

We use [Terraform](https://www.terraform.io/) to manage the required AWS resources for this experiment.

### Data

- [AWS Public Blockchain Data](https://aws.amazon.com/marketplace/pp/prodview-xv4ehzlgtim5a)

Schema can be found [here](https://github.com/aws-samples/digital-assets-examples/blob/main/analytics/consumer/schema/eth.md).

```bash
aws s3 ls aws-public-blockchain/v1.0/eth/transactions/
```

### AWS S3

We need a bucket to locate Athena query outputs.

Refer to [`./terraform/s3.tf`](../terraform/s3.tf) for details.

### AWS Glue

We need a Glue database and table for Athena to query the files on S3.

Refer to [`./terraform/glue.tf`](../terraform/glue.tf) for details.
