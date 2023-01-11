"""Read kedro config outside the session context.

This is to workaround the need to access globals/parameters outside nodes/pipelines api.
"""
import os
from pathlib import Path

from kedro.config import TemplatedConfigLoader
from kedro.framework.project import settings

_module_dir = Path(os.path.dirname(__file__)).absolute()
_conf_dir = str(_module_dir.parent.parent / settings.CONF_SOURCE)
_conf_loader = TemplatedConfigLoader(
    conf_source=_conf_dir,
    env="local",
    globals_pattern="*globals.yml",
)
parameters = _conf_loader.get("parameters.yml")
