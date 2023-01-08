# kedro-on-aws

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
