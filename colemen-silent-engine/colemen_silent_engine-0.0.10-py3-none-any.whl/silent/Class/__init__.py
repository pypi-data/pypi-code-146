# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import




import datetime
import ast
from dataclasses import dataclass
from string import Template
from typing import Iterable, Union

import colemen_utils as c
import silent.EntityBase as _eb


import silent.Class.Property as _prop
import silent.Method.Method as _method

import silent.se_config as config
log = c.con.log


@dataclass
class Class(_eb.EntityBase):

    # module:config._py_module_type = None
    # '''The module that this class belongs to'''

    _properties:Iterable[config._py_property_type] = None
    '''A dictionary of property instances associated to this class.'''


    _methods:Iterable[config._method_type] = None
    '''A dictionary of methods that belong to this class.'''

    _bases:Iterable[str] = None
    '''A list of classes that this class bases'''

    is_dataclass:bool = False
    '''True if this class is a dataclass'''

    # description:str = None
    # '''The description for this class's docblock'''

    init_body:str = None
    '''The body to apply to the init method.'''

    _type_name:str = None
    '''The type name of this class.'''

    # _args = None
    # _kwargs = None

    def __init__(self,main:config._main_type,module:config._py_module_type,name:str=None,
                description:str=None,bases:Union[str,list]=None,init_body:str=None,
                is_dataclass:bool=False,tags:Union[str,list]=None
            ):
        '''
            Represents a python class

            Arguments
            ------------------
            `main` {Main}
                The project that this class belongs to.

            `module` {Module}
                The module instance that this class belongs to.

            [`name`=None] {str}
                The name of this class

            [`description`=None] {str}
                The docblock description of this class

            [`bases`=None] {str,list}
                The class or list of classes that this class will extend

            [`init_body`=None] {str}
                The body of the __init__ method.

            [`is_dataclass`=False] {bool}
                True if this class is a dataclass

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
        kwargs= {}
        kwargs['main'] = main
        kwargs['module'] = module
        kwargs['name'] = name
        kwargs['description'] = description
        kwargs['init_body'] = init_body
        kwargs['is_dataclass'] = is_dataclass
        super().__init__(**kwargs)

        if isinstance(tags,(list,str)):
            self.add_tag(tags)
        # self.main:config._main_type = main

        self.bases = []
        self._properties = {}
        self._methods = {}

        if isinstance(bases,(list,str)):
            self.add_base(bases)

        if self.is_dataclass is True:
            self.module.add_import("dataclasses","dataclass")


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
            "is_dataclass":self.is_dataclass,
            "properties":[],
            "methods":[],
            "tags":self._tags,
        }

        for prop in self.properties:
            value['properties'].append(prop.summary)
        for method in self.methods:
            value['methods'].append(method.summary)


        return value

    def add_base(self,class_name:str):
        '''
            Add a base class that this class will extend.

            ----------

            Arguments
            -------------------------
            `class_name` {str,list}
                The class or list of classes that this class will extend


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-09-2023 10:48:25
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_base
            * @xxx [01-09-2023 10:49:08]: documentation for add_base
        '''

        if isinstance(class_name,(str)):
            class_name = class_name.split(",")
        for base in class_name:
            self.bases.append(base)
        # self.bases.append(class_name)





    @property
    def type_name(self)->str:
        '''
            Get the type_name for this class.

            This is used for type hinting, it is just the classname with "_type" suffixed.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 16:09:19
            `@memberOf`: __init__
            `@property`: type_name
        '''
        if self._type_name is not None:
            return self._type_name
        value = f"_{self.package.name.name}_{self.name.name}_type"
        return value

    @type_name.setter
    def type_name(self,value):
        '''
            Set the type_name property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 16:25:50
            `@memberOf`: __init__
            `@property`: type_name
        '''
        self._type_name = value

    @property
    def type_declaration(self)->str:
        '''
            The typevar declaration for this class

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 16:06:58
            `@memberOf`: __init__
            `@property`: type_declaration
        '''
        rand = f"_{c.rand.rand(6,digits=False)}"
        value = f'''    import {self.import_path} as {rand}
    {self.type_name} = _TypeVar('{self.type_name}', bound={rand}.{self.name.name})'''
        return value


    # ---------------------------------------------------------------------------- #
    #                                  PROPERTIES                                  #
    # ---------------------------------------------------------------------------- #

    def add_property(self,name:str,description:str=None,data_type:str=None,default=None,
                    private:bool=False,getter_body:str=None,tags:Union[str,list]=None,
                    prop:config._py_property_type=True,auto_gen:bool=False)->config._py_property_type:
        '''
            Add a property to this class
            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the property to add.

            `tags` {str,list}
                A list or string of tags to add the the property
                This can be a comma delimited list.

            [`data_type`=None] {str}
                The python data type stored in this property

            [`default`=None] {any}
                The default value to assign to this property

            [`description`=None] {str}
                The Docblock description for this property

            [`private`=False] {bool}
                True if this property is private to its class.

            [`getter_body`=None] {str}
                The body of the getter method the default will return the property.

            [`gen_getter_setter`=False] {bool}
                If True, this will automatically generate the getter and setter method for this property

            Return {Property}
            ----------------------
            The newly instantiated property.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-04-2023 09:23:52
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_property
            * @xxx [01-04-2023 09:26:32]: documentation for add_property
        '''
        prop = _prop.Property(
            self.main,
            self,
            name = name,
            data_type = data_type,
            default = default,
            description = description,
            private = private,
            getter_body = getter_body,
            tags = tags,
        )
        
        if private is True or self.is_dataclass is False:
            self.add_getter(name=prop.name.name,prop=prop)
            self.add_setter(name=prop.name.name,prop=prop)

        typetype = config.contains_typing_type(data_type)
        if typetype is not False:
            self.module.add_import(import_path="typing",subjects=typetype)

        self._properties[name] = prop

        return prop



    @property
    def properties(self)->Iterable[config._py_property_type]:
        '''
            Get a list of properties for this class.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 09:30:42
            `@memberOf`: __init__
            `@property`: properties
        '''
        value = list(self._properties.values())
        return value

    @property
    def property_names(self)->Iterable[str]:
        '''
            Get the property_names property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 07:37:35
            `@memberOf`: __init__
            `@property`: property_names
        '''
        value = [x.name.name for x in self.properties]
        return value

    @property
    def private_props(self)->Iterable[config._py_property_type]:
        '''
            Get the private properties for this class

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 09:28:10
            `@memberOf`: __init__
            `@property`: private_props
        '''
        value = []
        for prop in self.properties:
            if prop.is_private:
                value.append(prop)
        return value

    @property
    def _dataclass_properties(self)->Iterable[config._py_property_type]:
        '''
            Get a list of properties that are handled by the dataclass.

            These properties are assigned prior to the init method so that the dataclass will automatically handle
            the getters and setters.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 11:04:35
            `@memberOf`: __init__
            `@property`: _dataclass_properties
        '''
        if self.is_dataclass is False:
            return None
        value = []
        for prop in self.properties:
            value.append(prop)
        return value

    def get_property(self,name:str)->config._py_property_type:
        '''
            Retrieve a property from this class
            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the property to search for.

            Return {Property}
            ----------------------
            The property instance, if it exists, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-04-2023 09:02:11
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: get_property
            * @xxx [01-04-2023 09:02:58]: documentation for get_property
        '''
        if name in self._properties:
            return self._properties[name]
        if f"_{name}" in self._properties:
            return self._properties[f"_{name}"]


    def get_properties_by_tag(self,tag,match_all=False):
        '''
            Get the get_properties_by_tag property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 17:04:31
            `@memberOf`: __init__
            `@property`: get_properties_by_tag
        '''
        if isinstance(tag,(str)):
            tag = tag.split(",")

        value = []
        tags = c.arr.force_list(tag)
        for prop in self.properties:
            if prop.has_tag(tags,match_all):
                value.append(prop)
        return value



    # ---------------------------------------------------------------------------- #
    #                                    METHODS                                   #
    # ---------------------------------------------------------------------------- #

    def add_method(self,name:str,description:str=None,body:str=None,return_type:str=None,return_description:str=None,
                tags:Union[list,str]=None
            )->config._method_type:
        '''
            Add a method to this class.
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
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_method
            * @xxx [01-09-2023 10:15:24]: documentation for add_method
        '''
        # kwargs['name'] = name
        method = _method.Method(
            self.main,
            pyclass=self,
            package=self.package,
            name=name,
            description=description,
            body=body,
            return_type=return_type,
            return_description=return_description,
            is_class_method=True,
        )
        if isinstance(tags,(list,str)):
            method.add_tag(tags)

        self._methods[method.local_name] = method
        return method


    def add_getter(self,name:str,description:str=None,body:str=None,
                return_type:str=None,return_description:str=None,
                tags:Union[list,str]=None,prop:config._py_property_type=None
            )->config._method_type:
        '''
            Add a getter method to this class.
            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the method.

            [`description`=None] {str}
                The docblock description for this method.

            [`body`=None] {str}
                The body of the method.

            [`return_type`=None] {str}
                The type returned by this method

            [`return_description`=None] {str}
                A description of the return value

            [`tags`=None] {list,str}
                A tag or list of tags to add after it is instantiated.

            [`prop`=None] {Property}
                A reference to the property that is being retrieved.

            Return {Method}
            ----------------------
            The new method instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-04-2023 13:28:59
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_method
            * @TODO []: documentation for add_method
        '''
        # @Mstep [IF] if the prop was not provided
        if prop is None:
            # @Mstep [] attempt to retrieve the property by name.
            prop = self.get_property(name)

        # @Mstep [IF] if a property was provided or exists on this class already.
        if prop is not None:
            # @Mstep [] override the other settings with the property settings.
            name = prop.name.name
            description = f"Retrieve this {self.name.name}'s {prop.name.name} property value\n    {prop.description}"
            return_type=prop.data_type
            return_description=f"This {self.name.name}'s {name} property value."
            tags=["getter","method",self.module.name.name]






        if body is None:
            body = f"return self.{name}"

        # @Mstep [] instantiate the method.
        method = _method.Method(
            self.main,
            pyclass=self,
            package=self.package,
            name=name,
            description=description,
            body=body,
            return_type=return_type,
            return_description=return_description,
            tags=tags,
            prop=prop,
            is_getter=True,
            is_setter=False,
            is_class_method=True,
        )

        if prop is not None:
            prop.getter_method = method
            method.prop = prop


        # self.get_property(prop.name.name)
        self._methods[method.local_name] = method
        return method

    def add_setter(self,name:str,description:str=None,body:str=None,
                return_type:str=None,return_description:str=None,
                tags:Union[list,str]=None,prop:config._py_property_type=None
            )->config._method_type:
        '''
            Add a setter method to this class.
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

            [`prop`=None] {Property}
                A reference to the property that is being retrieved.

            Return {Method}
            ----------------------
            The new method instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-04-2023 13:28:59
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_method
            * @TODO []: documentation for add_method
        '''
        # @Mstep [IF] if the prop was not provided
        if prop is None:
            # @Mstep [] attempt to retrieve the property by name.
            prop = self.get_property(name)

        
        # @Mstep [IF] if a property was provided.
        if prop is not None:
            # @Mstep [] override the other settings with the property settings.
            name = prop.name.name
            description = f"Retrieve this {self.name.name}'s {prop.name.name} property value\n    {prop.description}"
            return_type=prop.data_type
            return_description=f"This {self.name.name}'s {name} property value."
            tags=["setter","method",self.module.name.name]

        if body is None:
            body = f"self.{name} = value\nreturn self.{name}"
        
        # @Mstep [] instantiate the method.
        method = _method.Method(
            self.main,
            pyclass=self,
            package=self.package,
            name=name,
            description=description,
            body=body,
            return_type=return_type,
            return_description=return_description,
            tags=tags,
            prop=prop,
            is_getter=False,
            is_setter=True,
            is_class_method=True,
        )
        if prop is not None:
            prop.setter_method = method
            method.prop = prop
            
        method.add_arg("value",description=f"The new {method.name.name} value",tags="arg,setter,method_argument")

        # self.get_property(prop.name.name)
        self._methods[method.local_name] = method
        return method

    def get_method(self,name:str,partial_match=False,is_getter:bool=False,is_setter:bool=False)->config._method_type:
        '''
            retrieve a method by its name

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the method to search for.

            [`partial_match`=True] {bool}
                If True, the method name must contain the searched name

            [`is_getter`=False] {bool}
                If True, this will only search for getter methods
                
            [`is_setter`=False] {bool}
                If True, this will only search for setter methods

            Return {Method}
            ----------------------
            The method instance, None if it is not found.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-06-2023 08:55:24
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: get_method
            * @xxx [01-06-2023 08:56:24]: documentation for get_method
        '''
        result = []
        
        if is_getter:
            get_loc_name = f"{name}____get"
            if get_loc_name in self._methods:
                return self._methods[get_loc_name]

        if is_setter:
            set_loc_name = f"{name}____set"
            if set_loc_name in self._methods:
                return self._methods[set_loc_name]
        
        
        if partial_match is False:
            if name in self._methods:
                return self._methods[name]

            get_loc_name = f"{name}____get"
            if get_loc_name in self._methods:
                return self._methods[get_loc_name]

            set_loc_name = f"{name}____set"
            if set_loc_name in self._methods:
                return self._methods[set_loc_name]
        else:
            for k,v in self._methods.items():
                if name in k:
                    return v

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
            if mod.has_tag(tag,match_all):
                value.append(mod)
        return value

    def get_getter_setter_by_prop(self,prop_name:str)->Iterable[config._method_type]:
        prop = self.get_property(prop_name)
        if prop is not None:
            return [prop.getter_method,prop.setter_method]
        else:
            c.con.log(f"Failed to locate property {prop_name} on class {self.name.name}","warning")


    @property
    def method_names(self)->Iterable[str]:
        '''
            Get a list of method names associated to this class.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 07:38:46
            `@memberOf`: __init__
            `@property`: method_names
        '''

        value = [x.name for x in self.methods]
        return value

    @property
    def methods(self)->Iterable[config._method_type]:
        '''
            Get a list of method instances associated to this class.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 13:37:45
            `@memberOf`: __init__
            `@property`: methods
        '''
        value = list(self._methods.values())
        return value


    @property
    def _gen_getter_setter_methods(self):
        value = []

        for prop in self.properties:
            res = self.get_getter_setter_by_prop(prop.name.name)
            
            if res[0] is not None:
                value.append(ast.unparse(res[0].declaration_ast))
            if res[1] is not None:
                value.append(ast.unparse(res[1].declaration_ast))
        return '\n'.join(value)

    @property
    def _gen_getter_methods(self):
        '''
            Get the _gen_getter_methods property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 13:33:41
            `@memberOf`: __init__
            `@property`: _gen_getter_methods
        '''
        value = []
        for method in self.methods:
            if method.is_getter:
                value.append(ast.unparse(method.declaration_ast))
        return '\n'.join(value)

    @property
    def _gen_setter_methods(self):
        '''
            Get the _gen_setter_methods property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 13:33:41
            `@memberOf`: __init__
            `@property`: _gen_setter_methods
        '''
        value = []
        for method in self.methods:
            if method.is_setter:
                value.append(ast.unparse(method.declaration_ast))
        return '\n'.join(value)

    @property
    def _gen_misc_methods(self):
        '''
            Get the _gen_setter_methods property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 13:33:41
            `@memberOf`: __init__
            `@property`: _gen_setter_methods
        '''
        value = []
        for method in self.methods:
            if method.name.name == "__init__":
                continue
            if method.is_setter is False and method.is_getter is False:
                func_def =method.declaration_ast
                if isinstance(func_def,(str)):
                    value.append(func_def)
                    continue
                # print(ast.dump(method.declaration_ast,indent=4))
                value.append(ast.unparse(method.declaration_ast))
        return '\n'.join(value)




    @property
    def gen_init(self)->config._method_type:
        '''
            Get the __init__ method for this class or create it.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 14:29:44
            `@memberOf`: __init__
            `@property`: gen_init
        '''

        value = self.get_method("__init__")
        if value is None:
            initsuper = "super().__init__()" if len(self.bases) else ""

            ib = self.init_body
            if ib is None:
                ib = "pass"
            if len(initsuper) > 0:
                if "super().__init__" not in ib:
                    ib = f"{initsuper}\n{ib}"
                    # @Mstep [IF] if the last line of the body is "pass"
                    if ib.split("\n")[-1] == "pass":
                        # @Mstep [] remove the last line from the body.
                        ib = '\n'.join(ib.split("\n")[:-1])

            value = self.add_method(
                "__init__",
                description=self.description,
                body=ib
            )
        return value







    # @property
    # def _gen_bases(self):
    #     '''
    #         Generate a comma delimited list of classes that are extended by this class.

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 01-04-2023 09:37:05
    #         `@memberOf`: __init__
    #         `@property`: _gen_bases
    #     '''
    #     value = ""
    #     if len(self.bases) > 0:
    #         el = ','.join(self.bases)
    #         value = f"({el})"
    #     return value

    # ---------------------------------------------------------------------------- #
    #                                   __INIT__                                   #
    # ---------------------------------------------------------------------------- #



    def add_arg(self,name,**kwargs):
        '''
            Add an argument to this class's init method.

            If the name matches a property it will be automatically assigned in the __init__ method.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the argument.

            Keyword Arguments
            -------------------------
            [`data_type`=None] {str}
                The expected type of the argument

            [`default_value`=None] {any}
                The default value to use if no value is provided.

            [`description`=None] {any}
                The documentation description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-04-2023 14:46:25
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_arg
            * @xxx [01-05-2023 07:47:58]: documentation for add_arg
        '''
        value = self.gen_init
        value.add_arg(name,**kwargs)

    @property
    def arguments(self)->Iterable[config._method_argument_type]:
        '''
            Get the arguments property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 11:31:10
            `@memberOf`: __init__
            `@property`: arguments
        '''
        value = self.gen_init.arg_list
        return value

    def add_kwarg(self,name,**kwargs):
        '''
            Add a keyword argument to this class's init method.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the argument.


            Keyword Arguments
            -------------------------
            [`data_type`=None] {str}
                The expected type of the argument

            [`default_value`=None] {any}
                The default value to use if no value is provided.

            [`description`=None] {any}
                The documentation description


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-04-2023 14:45:43
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_kwarg
            * @TODO []: documentation for add_kwarg
        '''
        value = self.gen_init
        value.add_kwarg(name,**kwargs)

    def _apply_init_arg_assignments(self):
        '''
            Add property assignments when the init method has an argument with name matching a class property.

            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-05-2023 07:46:39
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: _apply_init_arg_assignments
            * @xxx [01-05-2023 07:47:43]: documentation for _apply_init_arg_assignments
        '''
        init = self.gen_init
        for arg in init.arg_list:
            for prop in self.properties:
                if arg.name.name == prop.name.name:
                    arg = init.get_arg(prop.name.name)
                    if arg is None:
                        continue
                    arg.data_type = prop.data_type
                    arg.description = prop.description
                    arg.default = prop.default
                    # print(f"init.body:{init.body}")
                    assign = prop.assign_result(arg.name.name,True)
                    # assign = f"self.{prop.attribute_name}{prop.attribute_type} = {arg.name.name}"
                    if assign not in init.body:
                        # @Mstep [IF] if the last line of the body is "pass"
                        if init.body.split("\n")[-1] == "pass":
                            # @Mstep [] remove the last line from the body.
                            init.body = '\n'.join(init.body.split("\n")[:-1])
                        # @Mstep [] concatenate the property assignment with the init body.
                        init.body=f"{init.body}\n{assign}"

                # if self.is_dataclass is False:
                #     assign = prop.assign_result(arg.name.name,True)
    @property
    def _gen_ast_bases(self):
        '''
            Get the _gen_ast_bases property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 11:57:15
            `@memberOf`: __init__
            `@property`: _gen_ast_bases
        '''
        bases = []
        for base in self.bases:
            bases.append(ast.Name(id=base,ctx=ast.Load()))
        return bases


    @property
    def ast(self):
        '''
            Get this class's ast object.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 11:40:02
            `@memberOf`: __init__
            `@property`: ast
        '''
        value = ast.ClassDef(
            name=self.name.name,
            bases=self._gen_ast_bases,
            keywords=[],
            body=[],
            decorator_list=[],
        )

        if self.is_dataclass is True:
            value.decorator_list.append(ast.Name(id='dataclass',ctx=ast.Load()))

        # xxx [01-05-2023 15:06:43]: apply properties to body
        if self.is_dataclass:
            for prop in self.properties:
                past = prop.declaration_ast
                if isinstance(past,(list)):
                    value.body = value.body + past
                else:
                    value.body.append(past)
        else:
            init = self.gen_init
            for prop in self.properties:
                if init.get_arg(prop.name.name) is not None:
                    continue

                assign = prop.assign_result(prop.default,True)
                if assign not in init.body:
                    # @Mstep [IF] if the last line of the body is "pass"
                    if init.body.split("\n")[-1] == "pass":
                        # @Mstep [] remove the last line from the body.
                        init.body = '\n'.join(init.body.split("\n")[:-1])
                    # @Mstep [] concatenate the property assignment with the init body.
                    init.body = f"{init.body}\n{assign}"

        self._apply_init_arg_assignments()
        # self.gen_init.Doc.description = self.description
        # self.gen_init.Doc.subject_name = self.name.name
        # xxx [01-05-2023 15:06:38]: apply init to body.
        value.body.append(self.gen_init.declaration_ast)

        # TODO []: apply methods to body
        # @Mstep [] add the custom getter methods
        value.body.append(ast.parse(self._gen_getter_setter_methods))
        # value.body.append(ast.parse(self._gen_getter_methods))

        # @Mstep [] add the custom setter methods
        # value.body.append(ast.parse(self._gen_setter_methods))

        # @Mstep [] add additional methods to the body
        value.body.append(ast.parse(self._gen_misc_methods))


        value = ast.fix_missing_locations(value)
        return value


    @property
    def result(self)->str:
        '''
            Get this class's source code.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 11:42:40
            `@memberOf`: __init__
            `@property`: result
        '''
        # value = self.result
        value = ast.unparse(self.ast)
        value = self.apply_auto_replaces(value)
        return value


    @property
    def instantiate_call(self):
        '''
            Get the statement used to instantiate this class.


            ClassName(some,args)

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 12:04:15
            `@memberOf`: __init__
            `@property`: instantiate_call
        '''
        return ast.unparse(self.instantiate_call_ast)

    # def instantiate_call(self,args:str=None):
    #     value = f"{self.name.name}({args})"
    #     value = ast.parse(value)
    #     return value

    @property
    def instantiate_call_ast(self):
        '''
            Get the instantiate_call_ast property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 12:04:15
            `@memberOf`: __init__
            `@property`: instantiate_call_ast
        '''

        args = ','.join([x.name.name for x in self.arguments])

        value = f"{self.name.name}({args})"
        value = ast.parse(value)
        return value


    # @property
    # def gen_init(self)->config._method_type:
    #     '''
    #         Get the __init__ method for this class or create it.

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 01-04-2023 14:29:44
    #         `@memberOf`: __init__
    #         `@property`: gen_init
    #     '''

    #     value = self.get_method("__init__")
    #     if value is None:
    #         init = self.add_method("__init__")

    #         initsuper = "super().__init__()" if len(self.bases) else ""

    #         ib = self.init_body
    #         if ib is None:
    #             ib = "pass"
    #         if len(initsuper) > 0:
    #             if "super().__init__" not in ib:
    #                 ib = f"{initsuper}\n{ib}"

    #         value = self.add_method(
    #             "__init__",
    #             description=self.description,
    #             body=ib
    #         )
    #     return value

    # @property
    # def result(self)->str:
    #     '''
    #         Generate the class declaration text.

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 01-04-2023 09:34:33
    #         `@memberOf`: __init__
    #         `@property`: result
    #     '''
    #     print(f"self.module:{self.module}")
    #     if self.is_dataclass is True:
    #         if self.module is not None:
    #             self.module.add_import("dataclass","dataclasses",None,True)
    #     dataclass_val = "@dataclass" if self.is_dataclass is True else ""
    #     self._apply_init_arg_assignments()
    #     # initsuper = "super().__init__()" if len(self.bases) else ""
    #     s = Template(config.get_template("class_template"))
    #     value = s.substitute(
    #         dataclass=dataclass_val,
    #         class_name=self.name,
    #         bases=self._gen_bases,
    #         dataclass_properties=self._dataclass_properties,
    #         init_method=self.gen_init.result,
    #         # initsuper=initsuper,
    #         getter_methods=self._gen_getter_methods,
    #         setter_methods=self._gen_setter_methods,
    #         misc_methods=self._gen_misc_methods,
    #         timestamp=datetime.datetime.today().strftime("%m-%d-%Y %H:%M:%S"),
    #     )
    #     return value





