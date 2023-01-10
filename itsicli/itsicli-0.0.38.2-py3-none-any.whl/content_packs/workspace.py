from pathlib import Path

from itsicli.content_packs.files import ContentPackConfig


def root_path():
    """
    Returns the best-guess root path for the content pack itsi dir, starting from the current working directory.

    :return: the root path for the given path
    :rtype: Workspace or None
    """
    curr = Path.cwd()

    while curr != curr.parent:
        config = curr.joinpath(ContentPackConfig.file_dir, ContentPackConfig.file_name)

        if config.exists():
            return curr

        curr = curr.parent

    return None
