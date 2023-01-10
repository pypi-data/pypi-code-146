""" MCLI Integration Local Directories """
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from mcli.api.exceptions import MCLIRunConfigValidationError
from mcli.models import MCLIIntegration
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob
from mcli.utils.utils_docker import DockerImage
from mcli.utils.utils_string_functions import validate_image

logger = logging.getLogger(__name__)


@dataclass
class MCLILocalIntegration(MCLIIntegration):
    """Local Directories Integration
    """

    directories: List[str]
    push_image: str
    docker_path: str = '.'
    docker_config: Optional[str] = None

    def __post_init__(self):
        # Force directories to be a list in case it is passed as a string in the yaml
        if isinstance(self.directories, str):
            self.directories = [self.directories]

        self._validate_directories_exist()
        self._validate_directories_relative_cwd()
        self._validate_docker_config_exists()
        self._validate_docker_push_image()

    def _validate_directories_exist(self) -> None:
        for directory in self.directories:
            path = Path(directory).expanduser().absolute()
            if not path.exists():
                raise MCLIRunConfigValidationError(f'Could not find directory in local integration: {path}')

            if not path.is_dir():
                raise MCLIRunConfigValidationError(
                    f'Expected {path} in local integration to be a directory, but found a file instead')

    def _validate_docker_config_exists(self) -> None:
        if self.docker_config is None:
            return

        config = Path(self.docker_config).expanduser().absolute()
        if not config.exists():
            raise MCLIRunConfigValidationError(f'Could not find docker config file for local integration: {config}')

        if not config.is_file():
            raise MCLIRunConfigValidationError(
                f'Expected {config} in local integration to be a file, but found a directory instead')

    def _validate_directories_relative_cwd(self):
        for directory in self.directories:
            path = Path(directory)
            if path.is_absolute():
                raise MCLIRunConfigValidationError(f'Directory must be a relative path, got {directory}')

            try:
                path.expanduser().absolute().relative_to(Path.cwd())
            except ValueError as e:
                raise MCLIRunConfigValidationError('Directories must be located with in the current working directory. '
                                                   f'{directory} is outside of {Path.cwd()}') from e

    def _validate_docker_push_image(self):
        if not validate_image(self.push_image):
            raise MCLIRunConfigValidationError(f'The image name "{self.push_image}" is not valid')

    def build_to_docker(self, image: str) -> None:
        """Add integration to docker image
        """
        docker_image = DockerImage(
            base_image=image,
            dest_image=self.push_image,
            config_file=self.docker_config,
        )
        docker_image.build_local_directories(directories=self.directories, path=self.docker_path)
        docker_image.push()
        docker_image.delete()

    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        """Add a integration to a job
        """
        kubernetes_job.container.image = self.push_image
        return True
