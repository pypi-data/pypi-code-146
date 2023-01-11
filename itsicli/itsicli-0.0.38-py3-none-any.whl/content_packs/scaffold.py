# ${copyright}

from itsicli.setup_logging import logger
from pathlib import Path


HERE = Path(__file__).resolve().parent

RESOURCES = HERE.joinpath('resources')


class Scaffolder(object):

    def __init__(self, root):
        self.root = root

    def create_file(self, filename):
        path = self.root.joinpath(filename)
        if path.exists():
            logger.info('{} already exists.'.format(path))
            return path

        template_path = RESOURCES.joinpath("template_{}".format(filename))
        if template_path.is_dir():
            logger.info('Creating directory at {} ...'.format(path))
            path.mkdir()
        else:
            logger.info('Creating file at {} ...'.format(path))
            contents = template_path.read_bytes()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(contents)

        return path
