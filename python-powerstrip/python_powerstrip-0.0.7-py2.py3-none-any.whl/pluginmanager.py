import logging
import collections
from pathlib import Path
from typing import Union

from powerstrip.utils import load_module
from powerstrip.models.plugin import Plugin
from powerstrip.models.metadata import Metadata
from powerstrip.models.pluginpackage import PluginPackage
from powerstrip.utils.utils import ensure_path
from powerstrip.exceptions import PluginManagerException


class PluginManager:
    """
    plugin manager
    """
    def __init__(
        self,
        plugins_directory: Union[str, Path],
        subclass: Plugin = Plugin,
        use_category: bool = False,
        auto_discover: bool = True,
        plugin_ext: str = ".psp",
        plugins_repo_directory: Union[str, Path] = "."
    ):
        """
        initialize the plugin manager class

        :param plugins_directory: directory where plugins are installed
        :type plugins_directory: Union[str, Path]
        :param subclass: subclass of Plugin that is managed by the
                         plugin manager, defaults to Plugin
        :type subclass: Plugin, optional
        :param category_subdir: use category subdirectories, defaults to False
        :type use_category: bool, optional
        :param auto_discover: if True, plugins will be discovered on startup,
                              defaults to True
        :type auto_discover: bool, optional
        :param plugin_ext: plugin extension name, defaults to ".psp"
        :type plugin_ext: str, optional
        :param plugins_repo_directory: repository directory where packed plugin
                                       packages are stored
        :type plugins_repo_directory: Union[str, Path]
        """
        self.plugins_directory = plugins_directory
        self.subclass = subclass
        self.use_category = use_category
        self.plugin_ext = plugin_ext
        self.plugins_repo_directory = plugins_repo_directory
        self.log = logging.getLogger(self.__class__.__name__)

        if auto_discover:
            # auto discover plugins from directory
            self.discover()

    @property
    def plugins_directory(self) -> Path:
        """
        returns the plugins directory where all plugins are installed

        :return: plugins directory
        :rtype: Path
        """
        return self._plugin_directory

    @plugins_directory.setter
    def plugins_directory(self, value: Union[str, Path]) -> None:
        """
        set the plugins directory

        :param value: plugins directory
        :type value: Union[str, Path]
        """
        # ensure that plugin_directory is a path
        self._plugin_directory = ensure_path(value)

        if not self._plugin_directory.exists():
            # plugin directory does not exist => create it
            self._plugin_directory.mkdir(parents=True)

    @property
    def plugins_repo_directory(self) -> Path:
        """
        returns the repository plugins directory where all
        packed plugins are located

        :return: repository plugins directory
        :rtype: Path
        """
        return self._plugins_repo_directory

    @plugins_repo_directory.setter
    def plugins_repo_directory(self, value: Union[str, Path]) -> None:
        """
        set the plugin repository directory

        :param value: repository plugins directory
        :type value: Union[str, Path]
        """
        # ensure that plugin_directory is a path
        self._plugins_repo_directory = ensure_path(value)

        if not self._plugins_repo_directory.exists():
            # plugin repo directory does not exist => create it
            self._plugins_repo_directory.mkdir(parents=True)

    @property
    def plugin_ext(self) -> str:
        """
        returns plugin extension

        :return: plugin extension
        :rtype: str
        """
        return self._plugin_ext

    @plugin_ext.setter
    def plugin_ext(self, value: str):
        """
        set plugin extension

        :param value: plugin extension
        :type value: str
        :raises PluginManagerException: raised if invalid extension
        """
        if not value.startswith("."):
            # leading '.' missing
            raise PluginManagerException(
                f"Invalid extension '{value}'!"
            )

        self._plugin_ext = value

    @property
    def categories(self) -> list:
        """
        return list of categories, i.e., list of subdirectories
        in plugin directory; if category is disabled return
        empty list

        :return: list of categories, if category is disabled empty list
        :rtype: list
        """
        if not self.use_category:
            # categories not used, return empty list
            return []

        return [
            directory.parents[1].name
            for directory in self.plugins_directory.glob(
                f"**/{Metadata.METADATA_FILENAME}"
            )
            if directory
        ]

    def _find_plugin_package(
        self,
        plugin_filename: Union[str, Path]
    ) -> Path:
        """
        try to find the plugin package by first using the given path directly
        then if not found, try to get the package from local path and the
        if still not found from the repository path

        :param plugin_filename: plugin package filename
        :type plugin_filename: Union[str, Path]
        :return: path of the plugin package file
        :rtype: Path
        """
        plugin_filename = ensure_path(plugin_filename)
        if plugin_filename.suffix != self.plugin_ext:
            # add correct plug suffix
            plugin_filename = plugin_filename.with_suffix(
                plugin_filename.suffix + self.plugin_ext
            )

        if plugin_filename.exists():
            # full path given and existing
            return plugin_filename

        # not found so try to find in local path or repo directory
        for path in (Path("."), self.plugins_repo_directory):
            fn = path.joinpath(plugin_filename.name)
            if fn.exists():
                # plugin package in the path found
                return fn

        # plugin package not found
        raise PluginManagerException(
            f"The plugin package '{plugin_filename}' could not be found!"
        )

    def get_plugin_classes(
        self,
        subclass: Plugin = None,
        category: str = None,
        tag: str = None
    ) -> dict:
        # if not provided, use originally define subclass
        subclass = subclass or self.subclass

        plugin_classes = collections.defaultdict(dict)
        for plugincls in subclass.__subclasses__():
            plugin = plugincls()

            match = True
            if (
                (subclass is not None) and
                not issubclass(plugincls, subclass)
            ):
                # subclass is not matching
                match = False

            if (
                (category is not None) and
                (category != plugin.metadata.category)
            ):
                # category is not matching
                match = False

            if (
                (tag is not None) and
                (len(plugin.metadata.tags) > 0) and
                (tag not in plugin.metadata.tags)
            ):
                # tag is not matching
                match = False

            if match:
                # matching search criteria then add to dict

                # get category or use 'default' as category
                cat = (
                    plugin.metadata.category
                    if self.use_category else
                    "default"
                )

                if plugin.metadata.name in plugin_classes[cat]:
                    # plugin with same name does already exist in category
                    raise PluginManagerException(
                        f"A plugin with the name '{plugin.metadata.name}' "
                        f"does already exist in the category '{cat}'!"
                    )

                # add plugin to the category
                plugin_classes[cat][plugin.metadata.name] = plugincls

        return plugin_classes

    def discover(
        self,
    ) -> None:
        """
        discover all plugins that are located in the plugins directory
        and that do match the given subclass
        """
        self.log.debug(
            f"Discovering all plugins in '{self.plugins_directory}'... "
        )
        for fn in self.plugins_directory.glob("**/*.py"):
            # derive from relative path the module name
            module_name = (
                fn.with_suffix("").relative_to(
                    self.plugins_directory
                ).as_posix()
            ).replace("/", ".")

            # load the module
            load_module(module_name, fn)

        # get all classes that are a subclass of the Plugin class
        plugin_classes = [
            plugincls
            for plugincls in Plugin.__subclasses__()
        ]
        self.log.debug(
            f"Found {len(plugin_classes)} plugins: "
            f"{', '.join([p.__name__ for p in plugin_classes])}"
        )

    def pack(
        self,
        directory: Union[str, Path],
        target_directory: Union[str, Path] = None,
        force: bool = False
    ) -> Path:
        """
        pack plugin from given source directory and store the
        resulting plugin package to the target directory or to the
        repository directory, if target directory is not provided

        :param directory: plugin source directory
        :type directory: Union[str, Path]
        :param target_directory: target directory to which packed plugin
                                 will be stored
        :type target_directory: Union[str, Path]
        :param force: if True, package will be installed even if it is already
                      existing, default: False
        :type force: bool
        :return: filename of the packed plugin
        :rtype: Path
        """
        return PluginPackage.pack(
            directory=directory,
            target_directory=(
                target_directory or
                self.plugins_repo_directory
            ),
            ext=self.plugin_ext,
            force=force
        )

    def info(self, plugin_filename: Union[str, Path]) -> dict:
        """
        get metadata information of the given plugin file

        :param plugin_filename: plugin filename
        :type plugin_name: Union[str, Path]
        :return: metata of the plugin
        :rtype: dict
        """
        # find the plugin package
        plugin_filename = self._find_plugin_package(plugin_filename)

        return PluginPackage.info(plugin_filename)

    def install(
        self,
        plugin_filename: Union[str, Path],
        force: bool = True
    ) -> Path:
        """
        install plugin from given filename

        :param plugin_filename: plugin filename
        :type plugin_filename: Union[str, Path]
        :param force: if True, package will be installed even if it has already
                      been installed previously, default: False
        :type force: bool
        :return: installed plugin directory
        """
        # find the plugin package
        plugin_filename = self._find_plugin_package(plugin_filename)

        return PluginPackage.install(
            plugin_filename=plugin_filename,
            target_directory=self.plugins_directory,
            use_category=self.use_category,
            force=force
        )

    def uninstall(
        self,
        plugin_name: str,
        category: str = None
    ) -> None:
        """
        uninstall the plugin with the given name

        :param plugin_name: plugin name
        :type plugin_name: str
        :param category: plugin's category
        :type category: str
        """
        PluginPackage.uninstall(
            plugin_name=plugin_name,
            target_directory=self.plugins_directory,
            category=category
        )

    def __repr__(self) -> str:
        """
        string representation of plugin manager

        :return: string representation of plugin manager
        :rtype: str
        """
        return (
            f"<PluginManager(plugins_directory='{self.plugins_directory}', "
            f"plugins_repo_directory='{self.plugins_repo_directory}', "
            f"use_category={self.use_category}, "
            f"subclass={self.subclass}, plugin_ext='{self.plugin_ext}')>"
        )
