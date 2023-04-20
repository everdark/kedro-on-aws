import os
import re
import shutil
import tarfile
import tempfile
from typing import Callable, Dict, Optional

import boto3
import joblib
import sagemaker
from sklearn.base import BaseEstimator

_AWS_REGION = "ap-southeast-1"
_MODEL_FILE_NAME = "model"
_INSTANCE_TYPE = "ml.m5.large"


def create_model_group_if_not_exist(name: str, desc: str = "") -> Dict:
    """Create a SageMaker Model Group if it does not already exist.

    Args:
        name: Name of the group.
        desc: Description of the group.

    Returns:
        API response.

    """
    args = {
        "ModelPackageGroupName": name,
        "ModelPackageGroupDescription": desc,
    }
    sess = boto3.Session()
    client = sess.client("sagemaker", region_name=_AWS_REGION)
    response = client.list_model_package_groups()
    _list = response.get("ModelPackageGroupSummaryList", [])
    model_groups = [g.get("ModelPackageGroupName") for g in _list]

    out = {}
    if name not in model_groups:
        out = client.create_model_package_group(**args)

    return out


def create_model_package(
    desc: str, model_group: str, model_url: str, image_uri: str
) -> str:
    """Create a SageMaker model package under a model group.

    Args:
        desc: Description of the model package.
        model_group: Name of a model group to register the model package.
        model_url: S3 path to a .tar.gz to locate model artifacts.
        image_uri: ECR path to a runtime image used by the model.

    Returns:
        ARN of the resulting model package.

    """
    args = {
        "InferenceSpecification": {
            "Containers": [
                {
                    "Image": image_uri,
                    "ModelDataUrl": model_url,
                }
            ],
            "SupportedContentTypes": ["application/x-parquet", "text/csv"],
            "SupportedResponseMIMETypes": ["application/x-parquet"],
        },
        "ModelPackageGroupName": model_group,
        "ModelPackageDescription": desc,
        "ModelApprovalStatus": "PendingManualApproval",
    }
    sess = boto3.Session()
    client = sess.client("sagemaker", region_name=_AWS_REGION)
    r = client.create_model_package(**args)
    return r["ModelPackageArn"]


def package_model_artifacts(
    model: BaseEstimator,
    models: Dict[str, Callable],
    model_desc: str,
    model_url: str,
    model_group_name: str,
    model_group_desc: str,
    image_uri: str,
) -> str:
    """Package model artifacts in SageMaker Model Registry compatible format.

    This function is used as a Kedro node function.
    The model will be read as a catalog item, save it to a local path to be
    tar.gz-ed then upload to S3 with any other artifacts for packaging purpose.

    Args:
        model: The latest pre-trained model.
        models: All versioned pre-trainined models (lazy-load).
        model_desc: Description of the model.
        model_url: S3 path to save the resulting artifacts.
        model_group_name: Name of the SageMaker Model Group.
        model_group_desc: Description of the SageMaker Model Group.
        image_uri: ECR path to a runtime image used by the model.

    Returns:
        ARN of the resulting model package.

    """
    # NOTE: the latest model should be the same as the model from the first argument,
    # we need that model as input to this node so that kedro will establish
    # a dependency such that the model registry only happens after model training
    versions = sorted(models.keys())
    latest_version = versions[-1]
    model: BaseEstimator = models[latest_version]()
    ver = os.path.dirname(latest_version)

    # save the pre-trained model to a temp dir
    tmpdir = tempfile.gettempdir()
    model_dir = tempfile.TemporaryDirectory()
    joblib.dump(model, f"{model_dir.name}/{_MODEL_FILE_NAME}")
    # also include the inference module
    shutil.copyfile("src/iris/inference.py", f"{model_dir.name}/inference.py")

    # package all model artifacts into a .tar.gz under system temp dir
    artifact_name = "model.tar.gz"
    model_tar_gz = f"{tmpdir}/{artifact_name}"
    with tarfile.open(model_tar_gz, "w:gz") as tar:
        for d, _, files in os.walk(model_dir.name):
            for f in files:
                tar.add(os.path.join(d, f), arcname=f)

    model_dir.cleanup()

    # upload model artifacts to s3
    sess = boto3.Session()
    s3_client = sess.client("s3", region_name=_AWS_REGION)
    model_s3_path = re.sub("^s3://", "", model_url).split("/")
    bucket = model_s3_path[0]
    prefix = "/".join(model_s3_path[1:])
    key = os.path.join(prefix, f"{ver}-{artifact_name}")
    _ = s3_client.upload_file(model_tar_gz, bucket, key)

    # register the model package
    _ = create_model_group_if_not_exist(model_group_name, model_group_desc)
    final_model_url = os.path.join(model_url, os.path.basename(key))
    model_arn = create_model_package(
        model_desc, model_group_name, final_model_url, image_uri
    )

    return model_arn


def create_model(name: str, arn: str, iam: Optional[str] = None) -> str:
    """Create a SageMaker model that can be used for either real-time serving or
    batch transform job.

    Reference:
        https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry-deploy.html

    Args:
        name: Model name.
        arn: Model ARN.
        iam: Execution role ARN.

    Returns:
        ARN of the resulting model.

    """
    if iam is None:
        iam = sagemaker.get_execution_role()

    args = {
        "ModelName": name,
        "ExecutionRoleArn": iam,
        "Containers": [
            {
                "ModelPackageName": arn,
                "Environment": {
                    "SAGEMAKER_PROGRAM": "inference.py",
                    "SAGEMAKER_SUBMIT_DIRECTORY": "/opt/ml/model",
                },
            }
        ],
    }
    sess = boto3.Session()
    client = sess.client("sagemaker", region_name=_AWS_REGION)
    r = client.create_model(**args)
    return r["ModelArn"]


def create_batch_transform_job(
    job_name: str, model_name: str, input_s3_prefix: str, output_s3_prefix: str
) -> Dict:
    """Create a SageMaker Batch Transform job.

    References:
        https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateTransformJob.html
        https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html

    Args:
        job_name: Name of the job.
        model_name: Name of the model to use.
        input_s3_prefix: S3 prefix to locate the input data files.
        output_s3_prefix: S3 prefix to locate the output data files.

    Returns:
        API response.

    """  # noqa: E501
    args = {
        "TransformJobName": job_name,
        "ModelName": model_name,
        "MaxPayloadInMB": 5,  # size of a single record
        "BatchStrategy": "MultiRecord",  # need to set SplitType
        "TransformInput": {
            "DataSource": {
                "S3DataSource": {
                    "S3DataType": "S3Prefix",
                    "S3Uri": input_s3_prefix,
                }
            },
            "ContentType": "application/x-parquet",
            "CompressionType": "None",
            # for parquet we should not split the file since they are treated as binary
            "SplitType": "None",
        },
        "TransformOutput": {
            "S3OutputPath": output_s3_prefix,
            "Accept": "application/x-parquet",
            "AssembleWith": "None",
        },
        "TransformResources": {
            "InstanceType": _INSTANCE_TYPE,
            "InstanceCount": 1,
        },
    }
    sess = boto3.Session()
    client = sess.client("sagemaker", region_name=_AWS_REGION)
    r = client.create_transform_job(**args)
    return r
