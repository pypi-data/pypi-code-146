import io
import logging
import shutil
import zipfile
import hashlib
from pathlib import Path
from typing import Union, List

from powerstrip.utils.utils import ensure_path, hash_directory
from powerstrip.models import Metadata
from powerstrip.exceptions import PluginPackageException


# prepare logger
log = logging.getLogger(__name__)


class PluginPackage:
    """
    plugin package
    """
    @staticmethod
    def pack(
        directory: Union[str, Path],
        target_directory: Union[str, Path],
        ext: str = ".psp",
        force: bool = False
    ) -> Path:
        """
        packs raw plugin from given directory and creates a plugin
        package based on the given target plugin package name.

        :param directory: directory with raw plugin content
        :type directory: Union[str, Path]
        :param target_directory: target directory of the plugin package
        :type target_directory: Union[str, Path]
        :param ext: name of the plugin package extension, default: .psp
        :type ext: str
        :param force: if True, package will be created even if it is already
                      existing, default: False
        :type force: bool
        :returns: name of the plugin package
        :type ext: Path
        :raises PluginPackageException: if plugin package is already existing
        """
        assert isinstance(directory, (str, Path))
        assert isinstance(target_directory, (str, Path))
        assert isinstance(ext, str) and ext.startswith(".")
        assert isinstance(force, bool)

        # ensure that directory is a Path and that it does exist
        directory = ensure_path(directory, must_exist=True)

        # load metadata from directory
        md = Metadata.create_from_directory(directory)

        # target directory must exist
        target_directory = ensure_path(target_directory, must_exist=True)

        # target directory must exist
        target_directory = ensure_path(target_directory, must_exist=True)

        # plugin package filename
        plugin_filename = target_directory.joinpath(
            f"{md.name.lower()}-{md.version}{ext}"
        )
        if (force is False) and plugin_filename.exists():
            # plugin package does already exist
            raise PluginPackageException(
                f"The plugin file '{plugin_filename}' does already exist!"
            )

        # define suffixes and files to exclude for plugin packing
        exclude_suffixes: list = [".pyc", ".bak", ".swp"]
        exclude_filenames: list = ["__pycache__", ".DS_Store"]

        # get directory's hash and save updated metadata back to file
        md.hash = hash_directory(
            directory=directory,
            exclude_suffixes=exclude_suffixes,
            exclude_filenames=exclude_filenames + [md.METADATA_FILENAME]
        ).hex()
        md.save_to_directory(directory)

        log.debug(f"Opening '{plugin_filename}'...")
        with zipfile.ZipFile(plugin_filename, "w") as zf:
            for fn in directory.glob("**/*"):
                if (
                    fn.suffix in exclude_suffixes or
                    fn.name in exclude_filenames
                ):
                    # skip unwanted extensions
                    continue

                log.debug(f"Adding '{fn}' to plugin package...")
                zf.write(fn, fn.relative_to(directory))

        return plugin_filename

    @staticmethod
    def install(
        plugin_filename: Union[str, Path],
        target_directory: Union[str, Path],
        use_category: bool = False,
        force: bool = False
    ) -> Path:
        """
        installs a plugin package from a given plugin file
        into the provided target directory

        :param plugin_filename: plugin filename
        :type plugin_filename: Union[str, Path]
        :param target_directory: target directory
        :type target_directory: Union[str, Path]
        :param use_category: if True, use category as subdirectory
        :type use_category: bool
        :param force: if True, package will be installed even if it has already
                      been installed previously, default: False
        :type force: bool

        :returns: target directory
        :type category: Path
        :raises PluginPackageException: when plugin file does not exist
        """
        assert isinstance(plugin_filename, (str, Path))
        assert isinstance(target_directory, (str, Path))
        assert isinstance(use_category, bool)
        assert isinstance(force, bool)

        # check that plugin filename is a Path and that it exists
        plugin_filename = ensure_path(plugin_filename, must_exist=True)

        # check that target directory a Path and that it exists
        target_directory = ensure_path(target_directory, must_exist=True)
        if not target_directory.is_dir():
            # invalid target directory
            raise PluginPackageException(
                f"Invalid target directory '{target_directory}'! Abort."
            )

        try:
            log.debug(f"Opening '{plugin_filename}'...")
            with zipfile.ZipFile(plugin_filename) as zf:
                # get metadata from metadata file within the plugin package
                with zf.open(Metadata.METADATA_FILENAME) as f:
                    metadata = Metadata.create_from_f(
                        io.TextIOWrapper(f)
                    )

                if not use_category:
                    # prepare target directory without category
                    target_directory = target_directory.joinpath(
                        metadata.name
                    )

                else:
                    # prepare target directory with category
                    target_directory = target_directory.joinpath(
                        metadata.category, metadata.name
                    )

                if (force is False) and target_directory.exists():
                    # plugin does already exist
                    raise PluginPackageException(
                        f"The plugin '{metadata.name}' does already "
                        f"exist in '{target_directory}'! Abort."
                    )

                log.debug(f"Installing plugin to '{target_directory}'...")

                # create plugin directory
                target_directory.mkdir(parents=True, exist_ok=True)

                # extract all files from plugin package to target directory
                zf.extractall(path=target_directory)

        except zipfile.BadZipFile as e:
            # not a zip file, i.e., not a valid plugin
            raise PluginPackageException(
                f"The file '{plugin_filename}' is not a valid plugin file!"
            )

        return target_directory

    @staticmethod
    def uninstall(
        plugin_name: str,
        target_directory: Union[str, Path],
        category: str = None
    ):
        """
        uninstall plugin package from ginve target directory

        :param plugin_name: name of the plugin
        :type plugin_name: str
        :param target_directory: target directory of the plugins
        :type target_directory: Union[str, Path]
        :param category: category that will be used as subdirectory
        :type category: str
        :raises PluginPackageException:
        """
        assert isinstance(plugin_name, str)
        assert isinstance(target_directory, (str, Path))
        assert (category is None) or isinstance(category, str)

        # ensure that target directory is a Path and that it does exist
        target_directory = ensure_path(target_directory, must_exist=True)

        if category is None:
            # get plugin directory without category
            plugin_directory = target_directory.joinpath(
                plugin_name
            )

        else:
            # get plugin directory with category
            plugin_directory = target_directory.joinpath(
                category, plugin_name
            )

        if not plugin_directory.exists():
            # plugin directory does not exist
            raise PluginPackageException(
                f"The plugin '{plugin_name}' is not installed "
                f"in '{target_directory}'! Abort."
            )

        # load metadata from directory
        md = Metadata.create_from_directory(plugin_directory)

        # remove the plugin directory
        log.debug(
            f"removing plugin directory '{plugin_directory}'..."
        )
        shutil.rmtree(plugin_directory)

    @staticmethod
    def info(
        plugin_filename: Union[str, Path]
    ) -> Metadata:
        """
        show info about plugin package from metadata file

        :param plugin_filename: plugin filename
        :type plugin_filename: Union[str, Path]
        :raises PluginPackageException: if, plugin file is broken
        :return: metadata with information about the plugin
        :rtype: Metadata
        """
        assert isinstance(plugin_filename, (str, Path))

        # check that plugin filename is a Path and that it exists
        plugin_filename = ensure_path(plugin_filename, must_exist=True)

        try:
            log.debug(f"Opening '{plugin_filename}'...")
            with zipfile.ZipFile(plugin_filename) as zf:
                # get metadata from metadata file within the plugin package
                with zf.open(Metadata.METADATA_FILENAME) as f:
                    metadata = Metadata.create_from_f(
                        io.TextIOWrapper(f)
                    )

                return metadata

        except zipfile.BadZipFile as e:
            # not a zip file, i.e., not a valid plugin
            raise PluginPackageException(
                f"The file '{plugin_filename}' is not a valid plugin file!"
            )
