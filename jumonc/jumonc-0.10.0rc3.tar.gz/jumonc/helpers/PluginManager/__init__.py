"""jumonc PluginManager!"""
import argparse
import importlib.util
import logging

import pluggy

from jumonc import settings
from jumonc.helpers.PluginManager import hookspec
from jumonc.models import pluginInformation

logger = logging.getLogger(__name__)



plugin_manager = pluggy.PluginManager("jumonc")
plugin_manager.add_hookspecs(hookspec)
plugin_manager.load_setuptools_entrypoints("jumonc")


def addPluginArgs(parser: argparse.ArgumentParser) -> None:
    addAllPathsAsPlugins()
    
    for plugin in plugin_manager.get_plugins():
        plugin_name = str(plugin_manager.get_name(plugin))
        parser.add_argument("--" + plugin_name.lower(),
                            dest=plugin_name,
                            help="arguments for the plugin: " + plugin_name,
                            default="",
                            type=str)
        

def evaluatePluginArgs(parsed:argparse.Namespace) -> None:
    argument_dic = vars(parsed)
    for plugin in plugin_manager.get_plugins():
        plugin_name = str(plugin_manager.get_name(plugin))
        plugin_arg_str = argument_dic[plugin_name]
        plugin_parser = plugin.startup_parameter_parser()
        
        plugin_parser.add_argument("--disable",
                            dest="DISABLE",
                            help="Allows to disable this plugin (" + plugin_name + " / " + str(plugin_manager.get_canonical_name(plugin)) + ")",
                            default=False,
                            action='store_true')

        
        plugin_parsed = plugin_parser.parse_args(plugin_arg_str.split())
        
        logger.debug("Plugin arguments for plugin %s: %s", plugin_name, str(plugin_parsed))
        
        if plugin_parsed.DISABLE:
            plugin_manager.unregister(plugin)
        else:
            plugin.evaluate_startup_parameter(plugin_parsed)


def addPathPlugin(pluginPath:str) -> None:
    try:
        spec = importlib.util.spec_from_file_location("module.name", pluginPath)
        if spec is not None:
            module = importlib.util.module_from_spec(spec)
            loader = spec.loader
            if loader is not None:
                loader.exec_module(module)
            
            plugin_manager.register(module)
    except Exception:
        logger.warning("User plugin \"%s\" can not be imported", pluginPath)


def addAllPathsAsPlugins() -> None:
    for path in settings.PLUGIN_PATHS:
        addPathPlugin(path)
        
        
def initPluginsREST() -> None:
    for plugin in plugin_manager.get_plugins():
        plugin_REST_paths = plugin.needed_REST_paths()
        for path in plugin_REST_paths:
            # TODO check path
            plugin.register_REST_path(path, path)

        
def logAllPlugins() -> None:
    for plugin in plugin_manager.get_plugins():
        logger.info("Using Plugin: \"%s\" with canonical name: \"%s\"", str(plugin_manager.get_name(plugin)), str(plugin_manager.get_canonical_name(plugin)))
    
    
def setPluginsWorkingStatus() -> None:
    for plugin in plugin_manager.get_plugins():
        works = plugin.selfcheck_is_working()
        pluginInformation.addPluginStatus(str(plugin_manager.get_canonical_name(plugin)), works)
