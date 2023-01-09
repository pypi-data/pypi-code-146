# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

'''
    A module containing the Module class declaration

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 01-06-2023 11:03:46
    `memberOf`: __init__
    `version`: 1.0
    `method_name`: Module
    * @TODO []: documentation for Module
'''


import datetime
from dataclasses import dataclass
import ast
from string import Template
import traceback
from typing import Iterable, Union

import colemen_utils as c

import silent.EntityBase as _eb

# import silent.Import.ImportStatement as _imp
from silent.Import import ImportStatement as _imp
from silent.DocBlock import ModuleDocBlock as _doc

import silent.Class as _class


import silent.se_config as config
log = c.con.log
import silent.Method.Method as _method


@dataclass
class Module(_eb.EntityBase):


    _methods:Iterable[config._method_type] = None
    '''A list of methods contained in the module'''

    _classes:Iterable[config._py_class_type] = None
    '''A dictionary of classes contained in this module'''

    _imports:Iterable[config._py_import_type] = None
    '''A list of import statement instances.'''

    # body:str= None
    # '''The user defined content to append to the body of the module'''

    methods:Iterable[config._method_type] = None

    def __init__(self,main:config._main_type,package:config._package_type,name:str,description:str,
                overwrite:bool=True,tags:Union[str,list]=None
        ):
        '''
            Represents a python module.

            ----------

            Arguments
            -------------------------

            `main` {Main}
                A reference to the project instance.

            `package` {Package}
                A reference to the package this module belongs to.

            `name` {str}
                The name of this module.

            `description` {str}
                The documentation description of this module

            [`overwrite`=True] {bool}
                If False, this file will not save over an already existing version.

            [`tags`=None] {list,str}
                A tag or list of tags to add after it is instantiated.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-26-2022 08:35:16
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: Table
            * @xxx [12-26-2022 08:36:08]: documentation for Table
        '''
        kwargs={}
        kwargs['main'] = main
        kwargs['package'] = package
        kwargs['name'] = name
        kwargs['description'] = description
        kwargs['overwrite'] = overwrite
        super().__init__(**kwargs)
        

        if isinstance(tags,(str,list)):
            self.add_tag(tags)

        self._classes = {}
        self._methods = []
        self._properties = {}
        self._imports = []
        self.Doc = _doc.ModuleDocBlock(self.main,self)




    @property
    def summary(self):
        '''
            Get the summary property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-06-2022 12:10:00
            `@memberOf`: __init__
            `@property`: summary
        '''
        value = {
            "name":self.name.name,
            "description":self.description,
            "imports":[],
            "classes":[],
            "methods":[],
            # "schema":self.table.database.database,
        }
        # value['imports'] = []
        for imp in self._imports:
            value['imports'].append(imp.summary)
        for cl in self.classes:
            value['classes'].append(cl.summary)
        for method in self.methods:
            value['methods'].append(method.summary)
        return value

    def save(self):
        path = self.file_path
        if c.file.exists(path):
            if self.overwrite is True:
                c.file.write(path,self.result)
        else:
            c.file.write(path,self.result)
        # c.file.write(self.file_path,self.result)


    # ---------------------------------------------------------------------------- #
    #                                    IMPORTS                                   #
    # ---------------------------------------------------------------------------- #


    def add_import(self,import_path=None,subjects=None,alias=None,is_standard_library=False,is_third_party=False)->config._py_import_type:
        '''
            Add an import statement to this module.

            ----------

            Arguments
            -------------------------

            [`import_path`=None] {str}
                The import path where the imported value is located.

            [`subjects`=None] {list,str}
                The subject or list of subjects to import

            [`alias`=None] {str}
                The alias to use for this import

            [`is_standard_library`=False] {bool}
                True if this import is from the python standard library.

            [`is_third_party`=False] {bool}
                True if this is importing from a third party library.



            Return {Import}
            ----------------------
            The new import statement instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-04-2023 10:19:47
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_import
            * @TODO []: documentation for add_import
        '''
        imp = None
        if import_path is not None:
            imp = self.get_import(import_path=import_path)
            if imp is not None:
                imp.add_subject(subjects)
                return imp
        # print(f"add import: {subjects}")
        i = _imp(
            main=self.main,
            package=self.package,
            module=self,
            import_path=import_path,
            alias=alias,
            is_standard_library=is_standard_library,
            is_third_party=is_third_party,
        )
        i.add_subject(subjects)
        self._imports.append(i)
        return i

    @property
    def standard_library_imports(self)->Iterable[config._py_import_type]:
        '''
            Get the standard_library_imports property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 10:26:05
            `@memberOf`: __init__
            `@property`: standard_library_imports
        '''
        std_imports = []
        for imp in self._imports:
            print(f"import:{imp.subjects}")
            if imp.is_standard_library:
                std_imports.append(imp)
        return std_imports

    @property
    def third_party_imports(self)->Iterable[config._py_import_type]:
        '''
            Get a list of third party import statement instances associated to this module.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 10:26:05
            `@memberOf`: __init__
            `@property`: thrd_party_imports
        '''
        std_imports = []
        for imp in self._imports:
            if imp.is_third_party:
                std_imports.append(imp)
        return std_imports

    @property
    def local_imports(self)->Iterable[config._py_import_type]:
        '''
            Get the local_imports property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 10:26:05
            `@memberOf`: __init__
            `@property`: local_imports
        '''
        std_imports = []
        for imp in self._imports:
            if imp.is_standard_library is False and imp.is_third_party is False:
                std_imports.append(imp)
        return std_imports

    @property
    def _import_statements(self):
        '''
            Get the _import_statements property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 10:21:03
            `@memberOf`: __init__
            `@property`: _import_statements
        '''
        std_imports = '\n'.join(list([x.result for x in self.standard_library_imports]))
        thrd_imports = '\n'.join(list([x.result for x in self.third_party_imports]))
        local_imports = '\n'.join(list([x.result for x in self.local_imports]))

        value = f"{std_imports}\n{thrd_imports}\n{local_imports}"
        return value

    def get_import(self,subject_name:str=None,import_path:str=None):
        
        for im in self._imports:
            if subject_name in c.arr.force_list(im.subjects):
                return im
            if import_path in c.arr.force_list(im.import_path):
                return im



    # ---------------------------------------------------------------------------- #
    #                                    CLASSES                                   #
    # ---------------------------------------------------------------------------- #


    def add_class(self,name:str,description:str=None,init_body:str=None,is_dataclass:bool=False,bases:Union[str,list]=None,
                tags:Union[str,list]=None)->config._py_class_type:
        '''
            Create a class instance and associate it to this module.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the class

            `description` {str}
                The documentation description of the class

            [`init_body`=None] {str}
                The body of the __init__ method.

            [`is_dataclass`=False] {bool}
                True if the class should be a dataclass.

            [`bases`=None] {str,list}
                The class or list of classes that this class will extend

            [`tags`=None] {list,str}
                A tag or list of tags to add after it is instantiated.


            Return {Class}
            ----------------------
            The class instance

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-05-2023 11:30:17
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_class
            * @xxx [01-05-2023 11:36:41]: documentation for add_class
        '''
        nclass = _class.Class(
            self.main,
            module=self,
            name=name,
            description=description,
            init_body=init_body,
            is_dataclass=is_dataclass,
            tags=tags,
            bases=bases,
        )

        # if bases is not None:
        #     if isinstance(bases,(str)):
        #         bases = bases.split(",")
        #     for base in bases:
        #         nclass.add_base(base)
        self._classes[name] = nclass
        return nclass

    @property
    def classes(self)->Iterable[config._py_class_type]:
        '''
            Get a list of class instances associated to this module

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 10:49:39
            `@memberOf`: __init__
            `@property`: classes
        '''
        value:Iterable[config._py_class_type] = list(self._classes.values())
        return value



    # ---------------------------------------------------------------------------- #
    #                                    METHODS                                   #
    # ---------------------------------------------------------------------------- #


    def add_method(self,name:str,description:str=None,body:str=None,return_type:str=None,return_description:str=None,
                tags:Union[list,str]=None)->config._method_type:
        '''
            Add a method to this module.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the method.

            [`description`=None] {str}
                The docblock description for this method.

            [`body`="pass"] {str}
                The body of the method.

            [`return_type`=None] {str}
                The type returned by this method

            [`return_description`=None] {str}
                A description of the return value

            [`tags`=None] {list,str}
                A tag or list of tags to add after it is instantiated.

            Return {Method}
            ----------------------
            The new method instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-04-2023 13:28:59
            `memberOf`: Module
            `version`: 1.0
            `method_name`: add_method
            * @xxx [01-06-2023 10:33:45]: documentation for add_method
        '''
        # kwargs['name'] = name
        method = _method.Method(
            self.main,
            module=self,
            package=self.package,
            name=name,
            description=description,
            body=body,
            return_type=return_type,
            return_description=return_description,
            tags=tags,
            is_getter=False,
            is_setter=False,
            is_class_method=False,
        )

        self._methods.append(method)
        return method


    @property
    def methods(self)->Iterable[config._method_type]:
        '''
            Get a list of methods that belong to this module.

            This does NOT include class methods only globally available methods.

            `default`:[]


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 11:24:35
            `@memberOf`: __init__
            `@property`: methods
        '''
        return self._methods





    # ---------------------------------------------------------------------------- #
    #                                  GENERATION                                  #
    # ---------------------------------------------------------------------------- #

    @property
    def ast(self)->ast.Module:
        '''
            Get this modules ast object.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 11:03:02
            `@memberOf`: __init__
            `@property`: ast
        '''
        value = ast.Module(body=[],type_ignores=[])

        for imp in self._imports:
            value.body.append(imp.ast)

        # if self._body is not None:
        #     value.body.append(ast.parse())

        # TODO []: apply global variables to body
        # xxx [01-06-2023 11:29:06]: apply classes to body
        for cl in self.classes:
            value.body.append(cl.ast)

        # xxx [01-06-2023 11:29:03]: apply functions to body
        for method in self.methods:
            value.body.append(method.declaration_ast)


        # @Mstep [] apply the module docblock to the body.
        value.body.insert(0,ast.Expr(value=ast.Constant(value=self.Doc.result)))
        value = ast.fix_missing_locations(value)
        return value

    @property
    def result(self):
        '''
            Get the result property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 11:49:00
            `@memberOf`: __init__
            `@property`: result
        '''
        try:
            value = ast.unparse(self.ast)
        except TypeError as e:
            # print(ast.dump(self.ast,indent=4))
            # traceback.print_stack()
            c.con.log(ast.dump(self.ast,indent=4),"error")
            c.con.log(e,"error")

        if self.body is not None:
            value = f"{value}\n{self.body}"
        value = self.apply_auto_replaces(value)
        return value

    # @property
    # def result(self):
    #     '''
    #         Get the result property's value

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 01-04-2023 09:34:33
    #         `@memberOf`: __init__
    #         `@property`: result
    #     '''
    #     module_name = self.name
    #     if module_name is None:
    #         if len(self.classes) > 0:
    #             clas:config._py_class_type = self.classes[0]
    #             module_name = clas.name

    #     description = "A module containing the stuff." if self.description is None else self.description



    #     s = Template(config.get_template("module_template"))
    #     value = s.substitute(
    #         classes=self._class_declarations,
    #         imports=self._import_statements,
    #         description=description,
    #         module_name=module_name,
    #         timestamp=datetime.datetime.today().strftime("%m-%d-%Y %H:%M:%S"),
    #     )
    #     # value = re.sub(r"^\s*$","\n",value)
    #     # value = re.sub(r"[\n]{3,}","\n\n",value)
    #     # value = re.sub(r"^[\t\s]\n","",value)

    #     return value



