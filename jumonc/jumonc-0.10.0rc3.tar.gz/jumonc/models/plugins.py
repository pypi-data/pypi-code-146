import importlib.util
import logging
from types import ModuleType
from typing import Dict
from typing import List

from jumonc import settings


logger = logging.getLogger(__name__)


Plugin_modules: List[ModuleType] = []
Plugin_REST_paths: Dict[str, ModuleType] = {}


def startPlugins() -> None:
    for pluginPath in settings.PLUGIN_PATHS:
        try:
            spec = importlib.util.spec_from_file_location("module.name", pluginPath)
            if spec is not None:
                module = importlib.util.module_from_spec(spec)
                loader = spec.loader
                if loader is not None:
                    loader.exec_module(module)
            
                Plugin_modules.append(module)
        except Exception:
            logger.warning("User plugin \"%s\" can not be imported", pluginPath)
            

def gatherRESTpaths() -> None:
    for plugin in Plugin_modules:
        try:
            RESTpaths: List[str] = plugin.getNeededRESTpaths()
            for path in RESTpaths:
                Plugin_REST_paths[path] = plugin
        except Exception:
            logger.warning("User plugin \"%s\" does not supply a (correct) getNeededRESTpaths() function ", str(plugin))
            

def _removePathsAlreadyInUse() -> None:
    #pylint: disable=import-outside-toplevel
    from jumonc.handlers.base import RESTAPI
    #pylint: enable=import-outside-toplevel
    
    routes: List[str] = [] # routes already registered
    removeKeys: List[str] = []
    
    for rule in RESTAPI.url_map.iter_rules():
        routes.append(rule.rule)
        
    for (key, module) in Plugin_REST_paths.items():
        if key in routes:
            logger.warning("User plugin has a path conflict, path: \"%s\" plugin \"%s\"", str(key), str(module))
            removeKeys.append(key)
            
    for key in removeKeys:
        del Plugin_REST_paths[key]
   

def registerRESTpaths() -> None:
    _removePathsAlreadyInUse()
    
    for (path, module) in Plugin_REST_paths.items():
        module.registerPath(path = path)
