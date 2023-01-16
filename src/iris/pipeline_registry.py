"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from iris.pipeline import create_dummy_pipeline, create_pipeline


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = {
        "__default__": create_dummy_pipeline(),
        "aws": create_pipeline(),
    }
    return pipelines
