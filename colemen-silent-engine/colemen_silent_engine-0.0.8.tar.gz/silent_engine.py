# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
# pylint: disable=import-outside-toplevel

from dataclasses import dataclass
from typing import Iterable, Union
import colemen_utils as c
import silent.se_config as config
import silent.Package as _package


@dataclass
class Main:
    project_name:str = None
    root_path:str = None

    def __init__(self):
        self._entities = {
            "packages":[],
            "modules":{},
            "imports":[],
            "classes":[],
            "methods":[],
            "properties":[],
        }
        # self._packages = []
        self.data = {}


    def master(self):
        print("master")

    @property
    def summary(self):
        '''
            Get this main's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 09:39:11
            `@memberOf`: main
            `@property`: summary
        '''
        value = {
            "packages":{}
        }

        for pkg in self.packages:
            value['packages'][pkg.name.name] = pkg.summary
        c.file.writer.to_json("tmp.json",value)
        return value

    def save(self):
        imports = []
        # print(f"{len(self.packages)}")
        for pkg in self.packages:
            pkg.save()
            imports.append(pkg.import_statement)
        imports = '\n'.join(imports)
        c.file.write(f"{self.root_path}/{self.project_name}/__init__.py",imports)

    def get_by_tag(self,tag,entity_type:str=None):
        results = []
        entity_type = c.string.to_snake_case(entity_type)
        tags = c.arr.force_list(tag)
        tags.sort()
        tags.sort(key=len, reverse=False)


        if entity_type not in self._entities:
            print(f"{entity_type} is not a recognized entity type.")
            return False


        for pkg in self.packages:
            if pkg.has_tag(tags):
                results.append(pkg)

        for mod in self.modules:
            if mod.has_tag(tags):
                results.append(mod)

        return results


    # ---------------------------------------------------------------------------- #
    #                                   PACKAGES                                   #
    # ---------------------------------------------------------------------------- #

    def add_package(self,name:str,description:str=None,overwrite:bool=True,
                    tags:Union[str,list]=None)->config._package_type:
        '''
            add a new package to this project.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the package

            [`description`=None] {str}
                The documentation description for the package.

            [`overwrite`=True] {bool}
                If False, this file will not save over an already existing version.

            [`tags`=None] {list,str}
                A tag or list of tags to add after it is instantiated.


            Return {Package}
            ----------------------
            The new package instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-05-2023 09:09:47
            `memberOf`: main
            `version`: 1.0
            `method_name`: add_package
            * @xxx [01-05-2023 09:11:21]: documentation for add_package
        '''
        pkg = self.get_package(name)
        if pkg is not None:
            return pkg

        file_path = f"{self.root_path}/{self.project_name}/{name}"
        pkg = _package.Package(
            self,
            name=name,
            description=description,
            file_path=file_path,
            overwrite=overwrite,
            tags=tags,
        )
        return pkg

    def get_package(self,name,default=None)->Iterable[config._package_type]:
        '''
            Retrieve a package by its name or import path.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name to search for.

            Return {Package}
            ----------------------
            The package instance upon success, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-06-2023 15:11:08
            `memberOf`: silent_engine
            `version`: 1.0
            `method_name`: get_package
            * @xxx [01-06-2023 15:11:54]: documentation for get_package
        '''
        result = []
        for pkg in self.packages:
            # print(f"pkg.import_path:{pkg.import_path}")
            if pkg.name.name == name:
                result.append(pkg)
            if pkg.import_path == name:
                result.append(pkg)

        if len(result) == 0:
            return default
        return result

    @property
    def packages(self)->Iterable[config._package_type]:
        '''
            Get a list of this project's packages

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 09:48:14
            `@memberOf`: main
            `@property`: packages
        '''
        # value = self._entities['packages']
        value = self._entities['packages']
        return value



    # ---------------------------------------------------------------------------- #
    #                                    MODULES                                   #
    # ---------------------------------------------------------------------------- #


    def get_modules_by_tag(self,tag:str)->Iterable[config._py_module_type]:
        '''
            Get this main's get_modules_by_tag

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 09:59:00
            `@memberOf`: main
            `@property`: get_modules_by_tag
        '''
        value = []
        for mod in self.modules:
            if mod.has_tag(tag):
                value.append(mod)
        return value

    def get_methods_by_tag(self,tag:Union[str,list],match_all:bool=False)->Iterable[config._method_type]:
        '''
            Retrieve all methods with matching tags
            ----------

            Arguments
            -------------------------
            `tag` {str,list}
                The tag or list of tags to search for.

            [`match_all`=False] {bool}
                If True, all tags provided must be found.

            Return {list}
            ----------------------
            A list of methods that contain the matching tags, an empty list if None are found.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-06-2023 10:02:34
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: get_methods_by_tag
            * @xxx [01-06-2023 10:04:42]: documentation for get_methods_by_tag
        '''

        value = []
        for mod in self.methods:
            if mod.has_tag(tag):
                value.append(mod,match_all)
        return value



    @property
    def modules(self)->Iterable[config._py_module_type]:
        '''
            Get a list of this project's modules

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 09:48:14
            `@memberOf`: main
            `@property`: modules
        '''
        value = list(self._entities['modules'].values())
        return value

    @property
    def classes(self)->Iterable[config._py_class_type]:
        '''
            Get a list of this project's classes

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 09:48:14
            `@memberOf`: main
            `@property`: classes
        '''
        value = self._entities['classes']
        return value


    @property
    def methods(self)->Iterable[config._method_type]:
        '''
            Get a list of this project's classes

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 09:48:14
            `@memberOf`: main
            `@property`: classes
        '''
        value = self._entities['methods']
        return value






















    def register(self,instance):
        from silent.Package import Package
        if isinstance(instance,Package):
            # print(f"Register new package: {instance.name.name}")
            self._entities['packages'].append(instance)

        from silent.Module import Module
        if isinstance(instance,Module):
            self._entities['modules'][instance.name.name] = instance

        from silent.Import import ImportStatement
        if isinstance(instance,ImportStatement):
            self._entities['imports'].append(instance)

        from silent.Class import Class
        if isinstance(instance,Class):
            self._entities['classes'].append(instance)

        from silent.Method.Method import Method
        if isinstance(instance,Method):
            self._entities['methods'].append(instance)

        from silent.Class.Property import Property
        if isinstance(instance,Property):
            self._entities['properties'].append(instance)


def new(project_name:str,root_path:str,**kwargs):
    m = Main()
    m.project_name = project_name
    m.root_path = root_path
    # m.use_random_type_names = c.obj.get_kwarg(['use_random_type_names'],True,(bool),**kwargs)
    return m



# if __name__ == '__main__':
#     m = Main()
#     m.master()

