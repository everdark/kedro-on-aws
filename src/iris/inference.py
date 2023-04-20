"""Custom inference module for SageMaker model serving purpose.
This module should be put as inference.py along with anyother model artifacts packaged
together as a .tar.gz on S3.
"""
import os
from io import BytesIO, StringIO
from typing import BinaryIO

import joblib
import pandas as pd
from botocore.response import StreamingBody
from sklearn.base import BaseEstimator


def model_fn(model_dir: str) -> BaseEstimator:
    """Model function to load a pre-trained model.

    Args:
        model_dir: Path to the model artifacts.

    Returns
        A pre-trained model object.

    """
    # we dont read model from model_dir since it is the output dir for a training job
    # we alrady provide our model in package and the default untar location is
    # /opt/ml/code
    print("list /opt/ml/code:")
    print(os.listdir("/opt/ml/code"))
    model = joblib.load(os.path.join("/opt/ml/code", "model"))
    return model


def predict_fn(data: pd.DataFrame, model: BaseEstimator) -> pd.DataFrame:
    """Prediction function."""
    yhat = model.predict(data)
    out = pd.DataFrame(yhat, columns=["predicted_score"], index=data.index)
    return out


def input_fn(
    input_data: StreamingBody, content_type: str = "application/x-parquet"
) -> pd.DataFrame:
    """Input function for processing incoming data before model prediction."""
    label_name = "species"
    if content_type == "application/x-parquet":
        data = BytesIO(input_data)
        df = pd.read_parquet(data)
    elif content_type == "text/csv":
        df = pd.read_csv(StringIO(input_data))
    else:
        raise ValueError("Expected `application/x-parquet` or `text/csv`.")

    if label_name in df.columns:
        df = df.drop(columns=[label_name])

    return df


def output_fn(output: pd.DataFrame, accept: str = "application/x-parquet") -> BinaryIO:
    """Output function for post-processing model prediction output."""
    if accept == "application/x-parquet":
        buffer = BytesIO()
        output.to_parquet(buffer)
        return buffer.getvalue()
    else:
        raise Exception("Requested unsupported ContentType in Accept: " + accept)
