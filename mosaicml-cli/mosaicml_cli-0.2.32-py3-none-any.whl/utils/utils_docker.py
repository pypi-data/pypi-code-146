"""Utils for accessing docker sdk"""
import contextlib
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, Generator, List, Optional, Set

import docker
from docker.errors import APIError
from rich.progress import Progress, SpinnerColumn
from rich.spinner import Spinner

from mcli.utils.utils_logging import console
from mcli.utils.utils_string_functions import docker_image_to_repo_tag

logger = logging.getLogger(__name__)

DEFAULT_PLATFORM = 'linux/amd64'


def load_docker_config(config_file: str) -> Dict[str, Optional[str]]:
    with open(config_file, encoding='utf8') as f:
        data = json.loads(f.read())

    if 'username' not in data:
        raise KeyError(f'Field \'username\' must be provided in {config_file}')
    if 'password' not in data:
        raise KeyError(f'Field \'password\' must be provided in {config_file}')

    config = {}
    for f in ('username', 'password', 'email', 'registry'):
        if f in data:
            config[f] = data[f]

    return config


def get_docker_client() -> docker.APIClient:
    """Get the docker client
    """
    return docker.from_env(assert_hostname=True)


def get_image_tags(client: docker.APIClient) -> Set[str]:
    """Gets all unique image tags available
    """
    tags = set()
    for image in client.images.list():
        for tag in image.tags:
            tags.add(tag)
    return tags


def _get_common_path(path1: Path, path2: Path) -> Optional[Path]:
    """Returns a common path of two paths if there is one
    """

    while path1 is not None:
        if str(path1) in ('.', '/'):
            break
        try:
            path2.relative_to(path1)
            return path1
        except ValueError:
            path1 = path1.parent

    return None


# Progress rendering methods
@contextlib.contextmanager
def show_progress() -> Generator[Progress, None, None]:
    """Context manager for stopping existing live displays (ie spinners) and showing a
    progress bar

    Raises:
        RuntimeError: Raise if there is no existing live display

    Yields:
        Rich progress bar object
    """
    # Stop existing live display
    live = console._live  # pylint: disable=protected-access
    if live is not None:
        live.stop()

    # Yield a progress bar, but don't show it if the console isn't rendering
    with Progress(SpinnerColumn(),
                  *Progress.get_default_columns(),
                  console=console,
                  transient=True,
                  disable=(live is None)) as progress:
        yield progress

    # Restart the existing live display
    if live is not None:
        live.start()


def is_rendering() -> bool:
    """Check if the stdout console is currently rendering a live display

    Returns:
        True if the console is currently rendering
    """
    return console._live is not None  # pylint: disable=protected-access


def spinner_update(message: str) -> None:
    """Update an existing live display spinner, if one exists

    Args:
        message: Message to use as the spinner's text
    """
    live = console._live  # pylint: disable=protected-access
    if live and isinstance(live.renderable, Spinner):
        spinner = live.renderable
        spinner.update(text=str(message))


@dataclass
class Dockerfile:
    """Abstracts components of a dockerfile to build
    """

    image: str
    base_image: str
    args: Dict[str, str] = field(default_factory=dict)
    copy: List[str] = field(default_factory=list)
    path: Optional[str] = None

    def get_copy_command(self, directory: str) -> str:
        d = Path(directory)

        path = Path(self.path or '.')
        common = _get_common_path(path, d)
        if common is not None:
            # import pdb; pdb.set_trace()
            docker_dir = path / d.relative_to(*common.parts)
        else:
            docker_dir = path / Path(directory)

        return f'COPY {directory} {docker_dir}'

    @property
    def contents(self) -> str:
        """Converts data into runnable Dockerfile text
        """
        lines = []
        lines.append(f'FROM --platform={DEFAULT_PLATFORM} {self.base_image}')

        for k, v in self.args.items():
            lines.append(f'ARG {k}="{v}"')

        for c in self.copy:
            lines.append(self.get_copy_command(c))

        contents = '\n'.join(lines)
        logger.debug(contents)
        return contents


class DockerImage:
    """Manage a docker image through the docker api

    Note, since docker pull/build/push steps can be quite slow, these methods will
    automatically update any `rich` spinners that are rendered. If `rich` is currently
    rendering a live display, then `push` and `pull` will also display a progress bar.
    """

    auth_config = None

    def __init__(
        self,
        base_image: str,
        dest_image: str,
        client: Optional[docker.APIClient] = None,
        config_file: Optional[str] = None,
    ):
        self.image = dest_image
        self.repo, self.tag = docker_image_to_repo_tag(dest_image)
        self.base_image = base_image

        if client is None:
            client = get_docker_client()
        self.client: docker.APIClient = client

        if config_file is not None:
            self.auth_config = load_docker_config(config_file)

    def pull(self, image: str):
        """Pull a docker image
        """
        # If we are in a rendered environment, pull with progress
        if not is_rendering():
            self.client.images.pull(image)
        else:
            client = docker.APIClient()  # use low level to get streaming pull logs
            total, progress_by_layer = 0, {}
            with show_progress() as progress:
                download = progress.add_task('Pulling base image locally ', total=0)
                for line in client.pull(image, stream=True, decode=True):
                    if 'progress' in line:
                        if line['id'] not in progress_by_layer:
                            total += line['progressDetail']['total']
                        progress_by_layer[line['id']] = line['progressDetail']['current']
                        progress.update(download, completed=sum(progress_by_layer.values()), total=total)

    def build(self, dockerfile: Dockerfile):
        """Builds a docker image using the dockerfile object provided
        """

        self.pull(self.base_image)

        spinner_update(f'Building new image {self.image} locally from {self.base_image}')
        with NamedTemporaryFile('w') as temp:
            temp.write(dockerfile.contents)
            temp.seek(0)
            client = docker.APIClient()  # use low level to get streaming pull logs
            for line in client.build(
                    tag=self.image,
                    path='.',  # relative path to look for dockerfile
                    dockerfile=temp.name,
                    nocache=False,
                    decode=True,
            ):
                if 'stream' in line:
                    spinner_update(f'Building new image {self.image} locally from {self.base_image} {line["stream"]}')
            logger.debug(f"Docker image {self.image} created from {self.base_image}")

    def build_local_directories(self, directories: List[str], path: str) -> None:
        """Builds local directories into a docker image
        """
        logger.debug(f'Creating local directory image for {self.image}')
        self.build(dockerfile=Dockerfile(
            image=self.image,
            base_image=self.base_image,
            copy=directories,
            path=path,
        ))

    def push(self):
        """Pushes a docker image to a docker repo
        """
        spinner_update(f'Pushing image {self.repo}:{self.tag}...')
        try:
            if self._will_overwrite_important_tag():
                raise RuntimeError(
                    f'The image {self.image} already exists and pushing will overwrite this particular image tag. '
                    f'Either remove the tag from the image name ({self.repo}) '
                    'or update the tag in `push_image` in the YAML')

            args = {
                'repository': self.repo,
                'tag': self.tag,
                'auth_config': self.auth_config,
                # stream the push to catch any errors (not all raise an APIError)
                'stream': True,
                'decode': True,
            }
            with show_progress() as progress:
                upload = progress.add_task(f'Pushing image {self.repo}:{self.tag} ', total=0)
                total, progress_by_layer = 0, {}
                for line in self.client.images.push(**args):
                    if 'errorDetail' in line:
                        raise RuntimeError(f'Failed to push to docker image: {line["errorDetail"]}')
                    if 'progress' in line:
                        if line['id'] not in progress_by_layer:
                            total += line['progressDetail']['total']
                        progress_by_layer[line['id']] = line['progressDetail']['current']
                        completed = sum(progress_by_layer.values())
                        progress.update(upload, completed=completed, total=total)
                        if progress.finished:
                            progress.reset(upload, description='Completing image push...', start=False)

            logger.debug(f"Docker image {self.image} pushed")
        except APIError as e:
            if e.status_code == 403:
                raise RuntimeError("Unauthorized docker push. Please ensure you are either logged in "
                                   "with `docker login` or have specified a valid `docker_config` in your YAML.") from e
            else:
                raise RuntimeError(e) from e

    def _will_overwrite_important_tag(self) -> bool:
        # allow overwrites to latest (default) tag
        if self.tag == 'latest':
            return False

        try:
            self.client.images.get_registry_data(self.image)
            return True
        except docker.errors.NotFound:
            return False

    def delete(self):
        """Delete the image locally
        """
        spinner_update(f'Cleaning up local image {self.image}...')
        self.client.images.remove(self.image)
