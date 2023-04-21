# Integration with SageMaker Model Registry and Batch Transform Job

Train a `scikit-learn` model (outside SageMaker) and save it as a versioned Kedro catalog.
Use catalog transcoding to obtain the model version string and re-package, upload to S3 as model artifacts.
Then create a SageMaker model package based on the artifacts.

- [Runtime Image](#runtime-image)
- [Approve Model Packages](#approve-model-packages)
- [Inference Module](#inference-module)

## Runtime Image

The image used for the model package is a pre-built SageMaker image for `scikit-learn`.
To pull that image:

```shell
REGION=ca-central-1
ACCOUNT_ID=341280168497
NAME=sagemaker-scikit-learn
TAG=1.2-1

aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com
docker pull ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${NAME}:${TAG}
```

## Approve Model Packages

To approve a model package using `aws-cli`:

```shell
ACCOUNT_ID=000000000000
MODEL_NAME=test
MODEL_VER=1
MODEL_ARN=arn:aws:sagemaker:ap-southeast-1:${ACCOUNT_ID}:model-package/${MODEL_NAME}/${MODEL_VER}
aws sagemaker update-model-package --model-package-arn ${MODEL_ARN} --model-approval-status Approved
```

To list all model packages and their approval status given a model group:

```shell
MODEL_GROUP=test
aws sagemaker list-model-packages --model-package-group-name ${MODEL_GROUP} \
    --query 'ModelPackageSummaryList[*].[ModelPackageArn,ModelApprovalStatus]'
```

Or to list all packages that are still pending approval:

```shell
MODEL_GROUP=test
aws sagemaker list-model-packages --model-package-group-name ${MODEL_GROUP} \
    --query 'ModelPackageSummaryList[?ModelApprovalStatus==`PendingManualApproval`]'
```

Once approved, a model package can be used to create a model ready for serving real-time or batch transform jobs.

To make sure model versioning from Kedro and SageMaker can be linked together,
we use versioned `JSONDataSet` to store ARN of the resulting AWS resources.

## Inference Module

Refer to [`../src/iris/inference.py`](./src/iris/inference.py) for details.
The module has been customized to allow input data in parquet format and also output prediction result in parquet.

This is refered to as a user module in the [`multi-model-server`](https://github.com/awslabs/multi-model-server) framework which is used by SageMaker training/inference image.
The actual implementation can be found in [`sagemaker-scikit-learn-container`](https://github.com/aws/sagemaker-scikit-learn-container).
Specifically, for the [model serving entrypoint](https://github.com/aws/sagemaker-scikit-learn-container/blob/master/src/sagemaker_sklearn_container/serving.py).
