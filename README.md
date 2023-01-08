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

The kedro template used in this repo is simply created by:

```bash
kedro new --starter=pyspark-iris
```

We use [Terraform](https://www.terraform.io/) to manage the required AWS resources.

To allow `pyspark` to read files from `s3`, we will need two jars:

- [hadoop-aws](https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws)
- [aws-java-sdk-bundle](https://mvnrepository.com/artifact/com.amazonaws/aws-java-sdk-bundle)

### AWS S3

We can query the source bucket directly.
Here instead we choose to copy some files to our own bucket as starting samples.

```bash
MY_BUCKET=k9-eth
REGION=ap-southeast-1

aws s3api create-bucket --bucket $MY_BUCKET --create-bucket-configuration LocationConstraint=$REGION
aws s3api put-public-access-block --bucket $MY_BUCKET \
    --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

aws s3 cp s3://aws-public-blockchain/v1.0/eth/transactions/date=2023-01-01 s3://$MY_BUCKET/transactions/date=2023-01-01 --recursive
aws s3 ls $MY_BUCKET --recursive
```

TODO: use terraform for this

### AWS Glue

```bash
GLUE_DB=eth
GLUE_TBL=transactions

aws glue create-database --database-input Name=$GLUE_DB
aws glue create-table --database-name $GLUE_DB --table-input Name=$GLUE_TBL
# now manually update the schmea from console using table_schema.json to save some cli hassles

aws glue update-table --database-name $GLUE_DB --table-input \
    '{ \
        "Name": "$GLUE_TBL", \
        "StorageDescriptor": {"Location": "$MY_BUCKET/transactions/"} \
    }'
```

TODO: use terraform for this
