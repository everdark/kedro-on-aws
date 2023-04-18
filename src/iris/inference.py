"""Custom inference module for SageMaker model serving purpose.
This module should be put as inference.py along with anyother model artifacts packaged
together as a .tar.gz on S3.

Reference:
https://docs.aws.amazon.com/sagemaker/latest/dg/adapt-inference-container.html
"""
import os
from io import BytesIO
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
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
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
    if content_type == "application/x-parquet":
        data = BytesIO(input_data)
        df = pd.read_parquet(data)
        return df
    else:
        raise ValueError("Expected `application/x-parquet`.")


def output_fn(output: pd.DataFrame, accept: str = "application/x-parquet") -> BinaryIO:
    """Output function for post-processing model prediction output."""
    if accept == "application/x-parquet":
        buffer = BytesIO()
        output.to_parquet(buffer)
        return buffer.getvalue()
    else:
        raise Exception("Requested unsupported ContentType in Accept: " + accept)
