"""
Bot sources module. Defines classes of distinct bot sources that behave
differently at the various steps of a factory functionality

Constants

    SUPPORTED_SOURCES:  Dictionary of <source_identifier>: <source_subclass>
"""
import importlib
import os
import re
import shutil
import subprocess
import hashlib
import sys
from pathlib import Path

try:
    import git
except ImportError:
    # ImportError: Most likely git is not in the expected place.  Not an issue
    #   unless the user wants to use bot_sources.GitBotSource
    pass
from click import BadParameter
from colorama import Fore

from pyqalx.core.errors import QalxFactoryValidationError, QalxFactoryBuildError
from pyqalx.core.utils import _msg_user


class BotSource:
    """
    Base class for source related functionality about a specific bot

    Instance attributes

        bot_name:       The bot name
        bot:            The entire bot definition from the plan
        build_path:     The bot build path
        md5_hash:       The md5_hash of the bot code
    """

    FORE = Fore.MAGENTA

    def __init__(self, bot_name, bot, build_path_dir, log, *args, **kwargs):
        self.bot_name = bot_name
        self.bot = bot
        self.source_dict = bot["source"]
        self.build_path = os.path.join(build_path_dir, bot_name)
        self.md5_hash = None
        self.log = log

    @staticmethod
    def get_source(bot):
        """
        Static method that accepts a bot definition and tries to identify
        the source type and return the appropriate BotSource subclass if found

        :param bot: The bot definition from the plan
        :return: The BotSource subclass if found

        :raises KeyError:     If no bot source subclass is identified
        """
        source = bot["source"]
        for key in source:
            bot_source_class = SUPPORTED_SOURCES.get(key.lower())
            if bot_source_class:
                return bot_source_class
        raise KeyError(f"Unknown bot source `{source}`")

    def _msg_user(self, msg, **kwargs):
        """
        Helper method that prints and also logs a debug message if a log
        instance attribute exists
        """
        _msg_user(
            title=self.bot_name, fore=self.FORE, msg=msg, log=self.log, **kwargs
        )

    def zip_build_path(self):
        """
        Zips the contents of the build_path. The name of the file is:
        "<name_of_build_path>.zip" and it is located in the parent folder of
        build_path

        :return: The path to the zip file created
        """
        return shutil.make_archive(self.build_path, "zip", self.build_path)

    @staticmethod
    def get_single_hash(file_path):
        """
        The an md5 hash for a single file. Bytes are read in chunks for a given
        file

        :param file_path: The path to the file to get an md5 hash for
        :return: The md5 hash
        """
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            # Reading the file in chunks to avoid reading the whole file in
            # memory: https://stackoverflow.com/a/3431838
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_hash(self):
        """
        Calculates the md5 hash of the contents of the build path, the value of
        which is stored under the md5_hash instance attribute
        """
        self.md5_hash = self._get_hash()

    def _get_hash(self):
        """
        Hook for calculating the md5 hash for each bot source type
        """
        self._msg_user("Calculating hash")
        hashes = []
        for root, _, files in os.walk(self.build_path):
            for file in files:
                fp = os.path.join(root, file)
                hashes.append(self.get_single_hash(fp))
        hasher = hashlib.md5()
        for hash_value in sorted(hashes):
            hasher.update(hash_value.encode("utf-8"))
        self._msg_user("Finished calculating hash")
        return hasher.hexdigest()

    def validate(self):
        """
        Hook for providing validation on a BotSource. Called by `download_bot`
        after the download has completed
        """
        self._validate_bot_path()

    def _validate_bot_path(self):
        """
        Validates that the bot_path is importable.  Adds the build_path to the
        path temporarily so that we can attempt the import.
        """
        from qalxcli.cli_types import BOT_IMPORT

        sys.path.append(self.build_path)

        def _remove_from_path():
            sys.path.remove(self.build_path)

        try:
            BOT_IMPORT(self.bot["bot_path"])
        except BadParameter as exc:
            # Checking if the exception is related to an ImportError through the
            # exception message. In such a case, we do not want to error, but
            # only warn the user that the build might fail later.
            if "No module named" in str(exc):
                module_regex = re.compile(".*No module named '(.*)'.*")
                module_name = module_regex.match(str(exc))[1]
                msg = (
                    f"'{module_name}' could not be imported during bot download"
                    ". Your factory build may fail. We have no way of knowing"
                )
                self._msg_user(msg)
            else:
                raise QalxFactoryValidationError(
                    f"Error validating `bot_path` on `{self.bot_name}`: {exc}"
                )
        finally:
            _remove_from_path()

    def _download_bot(self):
        """Hook for downloading a bot for a specific BotSource"""
        raise NotImplementedError("Must be implemented by subclass")

    def download_bot(self):
        bot = self._download_bot()
        self.validate()
        return bot

    def install_bot(self):
        """
        Install the bot code. This is needed for the bot code package and the
        dependencies to be correctly installed and configured
        """
        self._msg_user("Installing...")
        self._install_bot()
        self._msg_user("Finished Installing...")

    def _install_paths(self):
        """
        Starting at the same directory that the bot file resides in (the bottom
        of the tree), walk the path upwards until we get to the root of the
        build path.  Each of these directories `could` contain a setup.py,
        pyproject.toml or requirements.txt.
        :return: A `path.Path` instance where the install file `could` be
        """
        # Ensure we start at the lowest directory possible.
        # i.e. if user supplies the following:
        #       source:
        #         path: /path/to/factories/myfactory/my_bot_3_dir
        #       bot_path: deeply.nested.structure.my_bot_file_3:my_bot_3
        #
        # we start at: /the/build/path/my_bot_3/deeply/nested/structure
        # then walk upwards up to and including /the/build/path/my_bot_3/
        bot_file_dir = (
            self.bot["bot_path"].rpartition(".")[0].replace(".", os.path.sep)
        )
        install_path = Path(self.build_path, bot_file_dir)
        while install_path != Path(self.build_path).parent.absolute():
            # Walk up the tree until we're at the root of the build path
            yield install_path
            install_path = Path(install_path).parent.absolute()

    def _install_bot(self):
        """
        Hook for installing the bot code using pip and code that has been
        downloaded in the build path.  Walks from the bottom of the tree upwards
        until an install file has been found.  Once a file has been found and
        install has completed successfully we stop looking for further install
        files
        """
        for install_path in self._install_paths():
            # First try to install from `pyproject.toml` or `setup.py`.
            self._msg_user(
                "Attempting to install `setup.py` or `pyproject.toml` "
                f"from `{install_path}`"
            )
            output = subprocess.run(
                [shutil.which("pip"), "install", ".", "--upgrade"],
                cwd=install_path,
                check=False,
            )
            if output.returncode == 0:
                return
            self._msg_user(
                "Unable to install dependencies from `setup.py` "
                f"or `pyproject.toml` from `{install_path}`.  "
                f"Attempting to install from requirements file in `{install_path}`."
            )

            # The fallback option is to use the user defined requirements.txt file
            # if specified - failing that attempt to use a `requirements.txt` file
            # on `self.bot_path`
            requirements_path_key = "requirements_path"
            requirements_path = self.bot.get(
                requirements_path_key, "requirements.txt"
            )
            if requirements_path_key in self.bot and not os.path.exists(
                requirements_path
            ):
                # If the user has specified requirements we should check the
                # file exists
                msg = f"{requirements_path} does not exist."
                raise QalxFactoryBuildError(msg)
            output = subprocess.run(
                [
                    shutil.which("pip"),
                    "install",
                    "-r",
                    requirements_path,
                    "--upgrade",
                ],
                cwd=install_path,
                check=False,
            )

            if output.returncode == 0:
                return
            if os.path.exists(requirements_path):
                # The requirements path existed but there was an error installing.
                # An exception is raised so the user can go and fix it
                raise QalxFactoryBuildError(
                    f"An error occurred installing"
                    f" dependencies "
                    f"from {requirements_path}."
                )
            # There was no file found to install dependencies from in this
            # directory.  Continue walking the path upwards
            self._msg_user(
                f"No files found to install dependencies from in {install_path}."
            )
        # There was no file found to install dependencies from in any of the
        # searched directories.  This may be intentional but we have no way of
        # knowing.  Inform the user.
        self._msg_user(
            "No files found to install dependencies from."
            "  Dependencies not installed."
        )


class PathBotSource(BotSource):
    """
    Bot source class for code provide from a local path

    Instance attributes
        path:   The local path to the bot code
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = self.source_dict.get("path")

    def _download_bot(self):
        """
        Copies the local bot code to build_path
        """
        msg = f"Copying contents from `{self.path}` to `{self.build_path}`"
        self._msg_user(msg)
        shutil.copytree(self.path, self.build_path)


class GitBotSource(BotSource):
    """
    Bot source class for code provided from a url of a git repository

    Instance attributes
        url:   The url to the git repository with the bot code
    """

    def __init__(self, *args, **kwargs):
        # Ensure that the git is importable - required for GitBotSource to work
        importlib.import_module("git")

        super().__init__(*args, **kwargs)
        self.url = self.source_dict.pop("url")

    def _download_bot(self):
        """
        Downloads the bot code to build_path
        """
        msg = f"Cloning repository from `{self.url}` to `{self.build_path}`"
        self._msg_user(msg)
        git.Repo.clone_from(self.url, self.build_path, **self.source_dict)


class PyPIBotSource(BotSource):
    """
    Bot source class for code provided from a pypi repository

    Class attributes

        PYPI:   The key for pypi on the bot source
    """

    PYPI = "pypi"

    @staticmethod
    def install(source_dict):
        """
        method that allows easier installation of pypi sources for remote
        sectors
        :param source_dict:The source dict
        """
        pypi = source_dict.get(PyPIBotSource.PYPI)
        version = source_dict.get("version")
        if version is not None:
            pypi += f"=={version}"

        output = subprocess.run(
            [shutil.which("pip"), "install", pypi, "--upgrade"], check=False
        )
        if output.returncode != 0:
            raise QalxFactoryBuildError(f"Failed to install {pypi}")

    def zip_build_path(self):
        """
        pypi sources don't get downloaded - so there is nothing to zip
        """

    def _install_bot(self):
        """
        Pypi bots get installed directly from source
        """
        PyPIBotSource.install(self.source_dict)

    def _validate_bot_path(self):
        """
        bot_path cannot be validated for pypi as the package won't
        be installed so there is nothing that can be imported.
        """

    def _download_bot(self):
        """
        `pypi` sources don't get downloaded.  This is because, if the associated
        bot is for a remote sector the OS could be different - meaning that
        what is downloaded may not work on the remote sector.  Instead, these
        are just installed when `build` is called. An item will still be created
        but it won't have any data on it.
        """
        self._msg_user("Found pypi source.  Not downloading")

    def _get_hash(self):
        """
        Because no file is downloaded there is nothing to calculate a hash on.
        The API cannot be queried as the hashes are calculated for a specific
        file type (.tar.gz, .whl etc) so there is no way to be consistent.
        """
        self._msg_user("Found pypi source.  Not generating hash")


class QalxItemBotSource(BotSource):
    """
    Source class for Items that contain Bot code as a zip file.  Used by
    remote sectors to download and extract the bot code.

    Instance attributes

        bot_name:       The bot name
        bot:            The entire bot definition from the plan
        build_path:     The bot build path
        bot_code_item:  The ~pyqalx.Item instance that contains the zipped bot
                        code
    """

    def __init__(self, bot_code_item, *args, **kwargs):
        super(QalxItemBotSource, self).__init__(*args, **kwargs)
        self.bot_code_item = bot_code_item

    def _install_bot(self):
        if self.source_dict.get(PyPIBotSource.PYPI):
            # ensure pypi bots get installed in a specific way
            PyPIBotSource.install(source_dict=self.source_dict)
        else:
            super(QalxItemBotSource, self)._install_bot()

    def _download_bot(self):
        """
        Downloads the bot code from the Item and saves it in the appropriate
        build path for this bot.  Unzips the zip file.  Installs the bot
        """
        msg = f"Downloading bot code from API to `{self.build_path}`"
        self._msg_user(msg)
        if not os.path.exists(self.build_path):
            # The <bot_name> sub directory probably doesn't exist at bootstrap
            # time.  Ensure it gets created
            os.mkdir(self.build_path)

        if not self.source_dict.get(PyPIBotSource.PYPI):
            # Save the zipfile to disk.  Pypi bots won't have a file
            filename = self.bot_code_item.save_file_to_disk(self.build_path)
            # Unzip the zipped bot code into the build path.  This path will get
            # added to the PYTHONPATH at bot start time.
            shutil.unpack_archive(
                filename=filename, extract_dir=self.build_path
            )
        # Bots on remote instances should always be installed into the
        # environment immediately after downloading
        self.install_bot()
        # Return the bot_name as this is required for starting the bot
        return self.bot_name


SUPPORTED_SOURCES = {
    "url": GitBotSource,
    "path": PathBotSource,
    "pypi": PyPIBotSource,
}
