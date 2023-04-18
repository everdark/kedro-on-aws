import logging
from typing import List

from kedro.framework.cli.hooks import cli_hook_impl
from kedro.framework.startup import ProjectMetadata

logger = logging.getLogger(__name__)


class CLIHooks:
    @cli_hook_impl
    def before_command_run(
        self,
        project_metadata: ProjectMetadata,
        command_args: List[str],
    ) -> None:
        """Hooks to be invoked before a CLI command runs.
        It receives the ``project_metadata`` as well as
        all command line arguments that were used, including the command
        and subcommand themselves.

        Args:
            project_metadata: The Kedro project's metadata.
            command_args: The command line arguments that were used.
        """
        raise ValueError("?")  # FIXME: this hook is never run
        global test_hook_var
        test_hook_var = "changed-by-cli-hooks"
        logger.info(f"command line read from hooks: {command_args}")


cli_hooks = CLIHooks()
