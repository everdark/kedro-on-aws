"""
This is a boilerplate pipeline
generated using Kedro 0.18.4
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import dummy, print_dummy, read_raw_data, train_model
from iris.sagemaker import package_model_artifacts


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=read_raw_data,
                inputs=["transactions", "parameters"],
                outputs="parsed",
                name="parse_transactions",
            ),
        ]
    )


def create_dummy_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=dummy,
                inputs=["dummy", "parameters"],
                outputs="dummy_out",
                name="parse_dummy",
            ),
            node(
                func=print_dummy,
                inputs=["dummy_out"],
                outputs=None,
                name="print_dummy",
            ),
            node(
                func=train_model,
                inputs=["dummy"],
                outputs="model",
                name="train",
            ),
            node(
                func=package_model_artifacts,
                inputs={
                    "model": "model",
                    "models": "models",
                    "model_desc": "params:sagemaker.model_desc",
                    "model_url": "params:sagemaker.model_url",
                    "model_group_name": "params:sagemaker.model_group_name",
                    "model_group_desc": "params:sagemaker.model_group_desc",
                    "image_uri": "params:sagemaker.image_uri",
                },
                outputs=None,
                name="register_model"
            )
        ]
    )
