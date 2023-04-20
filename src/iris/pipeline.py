from kedro.pipeline import Pipeline, node, pipeline

from iris.sagemaker import create_model, package_model_artifacts

from . import nodes as N

node_train_model = node(
    func=N.train_model,
    inputs=["iris"],
    outputs="model",
    name="train_model",
)
node_package_model_artifacts = node(
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
    outputs="model_package_arn",
    name="register_model",
)
node_create_model = node(
    func=create_model,
    inputs={
        "model_package_arn": "model_package_arn",
        "model_name": "params:sagemaker.model_name_base",
    },
    outputs="model_arn",
    name="create_model",
)

pipeline_train_and_register_model = pipeline(
    [
        node_train_model,
        node_package_model_artifacts,
    ]
)
pipeline_create_model = pipeline(
    [
        node_create_model,
    ]
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=N.read_raw_data,
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
                func=N.dummy,
                inputs=["dummy", "parameters"],
                outputs="dummy_out",
                name="parse_dummy",
            ),
            node(
                func=N.print_dummy,
                inputs=["dummy_out"],
                outputs=None,
                name="print_dummy",
            ),
        ]
    )
