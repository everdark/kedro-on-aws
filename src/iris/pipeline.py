"""
This is a boilerplate pipeline
generated using Kedro 0.18.4
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import read_raw_data


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
