import os
import importlib
import pkgutil
import sys
import importlib
from pathlib import Path
from coinlib import Registrar

class PluginLoader:

    def __init__(self, parentdirectory=""):
        self.registrar = Registrar.Registrar()
        self.parentDirectory = parentdirectory
        return None

    def loadChildModules(self, module):
        pass

    def hasPlugins(self):
        return True

    def logger(self):
        return self.registrar.logger

    def loadPlugins(self):
        if not self.hasPlugins():
            return False
        dirname = self.parentDirectory + self.getLoaderPath()
        self.logger().info("Loading plugins from "+ str(dirname))
        ##for importer, package_name, _ in pkgutil.iter_modules([dirname]):

        def onerror(name):
            self.registrar.logger.error("Error importing module %s" % name)
            type, value, traceback = sys.exc_info()
            self.registrar.logger.error(traceback)

        for loader, package_name, is_pkg in pkgutil.walk_packages([dirname], onerror=onerror):
            replaced_dirname = dirname.replace("/", ".")
            full_package_name = '%s.%s' % (replaced_dirname, package_name)
            if package_name not in sys.modules:
                self.logger().info("Package is not in sys.modules "+package_name)
                self.logger().info(dirname)
                self.loadPlugin(dirname+"/"+package_name)

        pass

    def reloadPlugins(self):
        if not self.registrar.isLiveEnvironment():
            return False
        if not self.hasPlugins():
            return False
        dirname = self.getLoaderPath()
        for importer, package_name, _ in pkgutil.iter_modules([dirname]):
            full_package_name = '%s.%s' % (dirname, package_name)
            self.logger().info(full_package_name)
            self.reloadPlugin(dirname+"/"+package_name)

        return True

    def reloadPlugin(self, path):
        if not self.registrar.isLiveEnvironment():
            return False
        ret = False
        try:
            try:
                del sys.modules[path]
            except:
                pass

            # ret = __import__('%s' % path, globals=globals())
            base = os.path.basename(path)
            dirname = path.split("/")[0]
            path_comp = Path(path)
            moduleName = os.path.splitext(base)[0]
            sys.path.insert(0, dirname)
            self.registrar.currentPluginLoading = moduleName
            ret = __import__('%s' % moduleName, globals=globals())
            self.logger().info("Reimported plugin: "+moduleName)
            self.registrar.currentPluginLoading = None
        except Exception as e:
            self.registrar.currentPluginLoading = None
            self.logger().warning("ERror loading", str(e))
            pass
        return ret
        ##mod = importlib.import_module('%s' % path)
        ##return mod

    def loadPluginForTest(self, type, path):
        return self.loadPlugin(path)

    def loadPlugin(self, path):
        ret = None
        try:
            #ret = __import__('%s' % path, globals=globals())

            base = os.path.basename(path)
            dirname = os.path.dirname(path)
            path_comp = Path(path)
            moduleName = os.path.splitext(base)[0]
            sys.path.insert(0, dirname)
            self.registrar.currentPluginLoading = moduleName
            ret = __import__('%s' % moduleName, globals=globals())
            self.logger().info("Imported plugin: "+moduleName)
            self.registrar.currentPluginLoading = None

            #with open(path+".py", 'rb') as fp:
            #    globals()[moduleName] = importlib.import_module(moduleName, fp)
        except Exception as e:
            self.registrar.currentPluginLoading = None
            self.logger().warning("Error loading", e)
            return e

        return ret
        ##mod = importlib.import_module('%s' % path)
        ##return mod






