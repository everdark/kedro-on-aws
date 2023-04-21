"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from iris.pipeline import (
    create_dummy_pipeline,
    pipeline_athena,
    pipeline_create_model,
    pipeline_train_and_register_model,
)


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.

    """
    pipelines = {
        "__default__": create_dummy_pipeline(),
        "train_and_register_model": pipeline_train_and_register_model,
        "deploy_model": pipeline_create_model,
        "athena": pipeline_athena,
    }
    return pipelines
