# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import




from dataclasses import dataclass
import re
from string import Template
from typing import Iterable, Union
import datetime
import ast

import colemen_utils as c
import silent.EntityBase as _eb

import silent.DocBlock.ClassMethodDocBlock as _docblock
import silent.Method.MethodArgument as _ma
# from config import column_type,_relationship_type,endpointdoc_type,route_type,root_directory,susurrus_type
import silent.se_config as config
log = c.con.log


@dataclass
class Method(_eb.EntityBase):



    body:str = None
    '''The method's body'''

    return_description:str = None
    '''A description of the return value'''

    return_type:str = None
    '''The type returned by this method'''

    _is_getter:bool = False
    '''If True the property decorator is added to the method'''

    _is_setter:bool = False
    '''If True the property setter decorator is added to the method'''

    indent:int = 0

    is_class_method:bool = False

    _args:Iterable[config._method_argument_type] = None
    _kwargs:Iterable[config._method_argument_type] = None


    def __init__(self,main:config._main_type,package:config._package_type,name:str,pyclass:config._py_class_type=None,module:config._py_module_type=None,
                description:str=None,body:str="pass",return_type:str=None,return_description:str=None,is_getter:bool=False,
                is_setter:bool=False,is_class_method:bool=False,tags:Union[str,list]=None):
        '''
            Class used to generate a python class method.
            ----------

            Arguments
            -------------------------
            `main` {_main_type}
                A reference to the master

            `name` {str}
                The name of this method.

            [`pyclass`=None] {Class}
                A reference to the class that this method belongs to.

            [`module`=None] {Module}
                A reference to the module that this method belongs to.

            [`description`=None] {str}
                The docblock description for this method.

            [`body`="pass"] {str}
                The body of the method.

            [`return_type`=None] {str}
                The type returned by this method

            [`return_description`=None] {str}
                A description of the return value

            [`is_getter`=False] {bool}
                If True the property decorator is added to the method

            [`is_setter`=False] {bool}
                If True the property setter decorator is added to the method

            [`is_class_method`=False] {bool}
                True if this method belongs to a class.
                
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
        kwargs = {}
        kwargs['main'] = main
        kwargs['package'] = package
        kwargs['name'] = name
        kwargs['pyclass'] = pyclass
        kwargs['module'] = module
        kwargs['description'] = description
        kwargs['body'] = body
        kwargs['return_type'] = return_type
        kwargs['return_description'] = return_description
        kwargs['is_getter'] = is_getter
        kwargs['is_setter'] = is_setter
        kwargs['is_class_method'] = is_class_method

        super().__init__(**kwargs)
        
        if isinstance(tags,(list,str)):
            self.add_tag(tags)
        # self.main:config._main_type = main
        # self.pyclass:config._py_class_type = pyclass
        self.Doc = None
        self._args = []
        self._kwargs = []
        # self.Doc = _docblock.ClassMethodDocBlock(self)


        # populate_from_dict(kwargs,self)

        if self.is_class_method is True:
            self.indent = 4
            self.add_tag(self.pyclass.name.name)
        # self.Doc.indent = self.indent + 4

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
            "is_class_method":self.is_class_method,
            "return_description":self.return_description,
            "return_type":self.return_type,
            "is_getter":self.is_getter,
            "is_setter":self.is_setter,
            "arguments":[],
            "keyword_arguments":[],
            "import_statement":self.import_statement,
        }
        for arg in self.arg_list:
            value['arguments'].append(arg.summary)


        return value


    @property
    def local_name(self)->str:
        '''
            Get this Method's local_name

            The local name is used by the class for distinguishing methods with the same name.
            Specifically, this solves the name collisions caused by getters and setters having the same
            name. It does this by applying a suffix:

            propname____get
            propname____set

            If this method is not a getter or setter, its normal name is returned.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 09:00:57
            `@memberOf`: Method
            `@property`: get_local_name
        '''
        if self.is_getter:
            return f"{self.name.name}____get"
        if self.is_setter:
            return f"{self.name.name}____set"
        return self.name.name


    @property
    def is_getter(self)->bool:
        '''
            Get the is_getter value.

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 10:09:11
            `@memberOf`: PostArg
            `@property`: is_getter
        '''
        value = self._is_getter
        return value

    @is_getter.setter
    def is_getter(self,value:bool):
        '''
            Set the is_getter value.

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 10:09:11
            `@memberOf`: PostArg
            `@property`: is_getter
        '''
        if value is True:
            self.add_tag("getter","setter")
        else:
            self.delete_tag("getter")
        self._is_getter = value

    @property
    def is_setter(self)->bool:
        '''
            Get the is_setter value.

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 10:16:05
            `@memberOf`: PostArg
            `@property`: is_setter
        '''
        value = self._is_setter
        return value

    @is_setter.setter
    def is_setter(self,value:bool):
        '''
            Set the is_setter value.

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-06-2023 10:16:05
            `@memberOf`: PostArg
            `@property`: is_setter
        '''
        if value is True:
            self.add_tag("setter","getter")
        else:
            self.delete_tag("setter")
        self._is_setter = value


    # ---------------------------------------------------------------------------- #
    #                                   ARGUMENTS                                  #
    # ---------------------------------------------------------------------------- #



    def add_arg(self,name:str,data_type:str=None,default="__NO_DEFAULT_PROVIDED__",
                description:str="",arg:config._method_argument_type=None,tags:Union[str,list]=None):
        '''
            Add an argument to this method.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the argument.

            [`data_type`=None] {str}
                The expected type of the argument

            [`default`="__NO_DEFAULT_PROVIDED__"] {any}
                The default value to use if no value is provided.

            [`description`=""] {any}
                The documentation description

            [`tags`=None] {list,str}
                A tag or list of tags to add to this package after it is instantiated.

            [`arg`=None] {Method_Argument}
                A method argument instance to copy.
                This is useful when you want to add the same argument to another method.


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-03-2023 15:41:59
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_arg
            * @xxx [01-03-2023 15:43:13]: documentation for add_arg
        '''

        ma = _ma.MethodArgument(
            main=self.main,
            method=self,
            name=name,
            arg = arg,
            data_type = data_type,
            default = default,
            description = description,
            tags = tags,
        )

        if ma.has_default:
            self._args.append(ma)
        else:
            self._args.insert(0,ma)
        # self._args.append(ma)


    def add_kwarg(self,name,**kwargs):
        '''
            Add a keyword argument to this method.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the argument.

            Keyword Arguments
            -------------------------
            [`data_type`=None] {str}
                The expected type of the argument
            [`default`=None] {any}
                The default value to use if no value is provided.
            [`description`=None] {any}
                The documentation description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-03-2023 15:41:59
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: add_arg
            * @xxx [01-03-2023 15:43:13]: documentation for add_arg
        '''


        # ma = _ma.MethodArgument(self.main,self)
        ma = _ma.MethodArgument(
            self.main,
            self,
            name=name,
            data_type = c.obj.get_kwarg(['data_type','type'],None,(str),**kwargs),
            default = c.obj.get_kwarg(['default_value','default'],"__NO_DEFAULT_PROVIDED__",None,**kwargs),
            description = c.obj.get_kwarg(['description'],"",None,**kwargs),
        )

        # data_type = c.obj.get_kwarg(['py_type','type'],None,(str),**kwargs)
        # default_value = c.obj.get_kwarg(['default_value','default'],"__NO_DEFAULT_VALUE_SET__",None,**kwargs)
        # description = c.obj.get_kwarg(['description'],"",None,**kwargs)
        # ma.name = name
        # ma.py_type = data_type
        # ma.default_value = default_value
        # ma.description = description

        if ma.has_default:
            self._kwargs.append(ma)
        else:
            self._kwargs.insert(0,ma)
        # self._args.append(ma)



    def get_arg(self,name:str):
        for arg in self.arg_list:
            if arg.name.name == name:
                return arg
        return None

    # @property
    # def _gen_args_result(self)->str:
    #     '''
    #         Generate the arguments list for this method.

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 01-03-2023 12:21:19
    #         `@memberOf`: __init__
    #         `@property`: args
    #     '''
    #     value = ""

    #     if len(self._args) > 0:
    #         args = []
    #         for arg in self._args:
    #             args.append(arg.result)
    #         alist = ','.join(args)
    #         value = f",{alist}"
    #     return value

    @property
    def arg_list(self)->Iterable[config._method_argument_type]:
        '''
            Get a list of method argument instances

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-03-2023 16:00:40
            `@memberOf`: __init__
            `@property`: arg_list
        '''
        value = self._args
        return value

    @property
    def kwarg_list(self)->Iterable[config._method_argument_type]:
        '''
            Get the kwarg_list property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-03-2023 16:23:06
            `@memberOf`: __init__
            `@property`: kwarg_list
        '''
        value = self._kwargs
        return value









    @property
    def _return_type(self):
        '''
            Get the _return_type property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-03-2023 12:02:39
            `@memberOf`: __init__
            `@property`: _return_type
        '''
        value = self.return_type
        if value is None:
            return ""
        if isinstance(value,(str)):
            value = c.string.strip(value,['-','>'])
            value = f"->{value}"
        return value

    @property
    def decorator(self):
        '''
            Get the decorator property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-03-2023 12:05:57
            `@memberOf`: __init__
            `@property`: decorator
        '''
        value = ""
        if self.is_getter is True:
            value = "@property"
        if self.is_setter is True:
            value = f"@{self.name}.setter"
        return value

    @property
    def _body(self):
        '''
            Get this Method's _body

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 14:14:46
            `@memberOf`: Method
            `@property`: _body
        '''
        value = self.body
        if value is None:
            return "pass"
        return value
            # return " "*(self.indent+4) + "pass"
        values = value.split("\n")
        # value = '\n'.join([f"{' '*(self.indent+4)}{x}" for x in values])
        value = '\n'.join([x for x in values])

        return value

    # @property
    # def result(self):
    #     '''
    #         Get the result property's value

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 12-28-2022 16:49:44
    #         `@memberOf`: __init__
    #         `@property`: result
    #     '''
    #     self.Doc.subject_name = self.name
    #     self.Doc.description = self.description
    #     s = Template(config.get_template("method_template"))
    #     value = s.substitute(
    #         decorator=self.decorator,
    #         timestamp=datetime.datetime.today().strftime("%m-%d-%Y %H:%M:%S"),
    #         method_name=self.name,
    #         return_type=self._return_type,
    #         body=self._body,
    #         arguments=self._gen_args_result,
    #         description=self.description,
    #         docblock=self.Doc.result,
    #     )
    #     value = re.sub(r"[\s\n]*Meta","\n\n            Meta",value)
    #     value = re.sub(r":[\s\n]*'''",":\n        '''",value)
    #     return value


    @property
    def _gen_return_type(self):
        '''
            Get this Method's _gen_return_type

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 15:54:20
            `@memberOf`: Method
            `@property`: _gen_return_type
        '''
        if self.return_type is None:
            return ast.Constant(value=None)


        value = ast.Attribute(ctx=ast.Load())
        types = self.return_type.split(".")
        if len(types) == 1:
            # value.value = ast.Name(id=types[0], ctx=ast.Load())
            return ast.Name(id=types[0], ctx=ast.Load())

        if len(types) == 2:
            value.value=ast.Attribute(
                value=ast.Name(id=types[0], ctx=ast.Load()),
                attr=types[1],
                ctx=ast.Load()
            )
        if len(types) > 2:
            ann = ast.Attribute(
                value=ast.Name(id=types[0], ctx=ast.Load()),
                attr=types[1],
                ctx=ast.Load()
            )
            # @Mstep [] remove the first and second element.
            types = types[2:]

            for typ in types:
                ann=ast.Attribute(
                    value=ann,
                    attr=typ,
                    ctx=ast.Load()
                )

            value.value = ann
        return value

    @property
    def declaration_ast(self):
        '''
            Get this Method's ast

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 12:34:44
            `@memberOf`: Method
            `@property`: ast
        '''

        # return_type = ast.parse(self.return_type) if self.return_type is not None else ast.Constant(value=None)
        value = ast.FunctionDef(
            name=self.name.name,
            args=ast.arguments(
                posonlyargs=[],
                args=[],
                kwonlyargs=[],
                kw_defaults=[],
                # TODO []: add **kwargs to method.
                kwarg=[],
                defaults=[]),
            body=[],
            decorator_list=[],
            returns=self._gen_return_type
        )
        # if self.return_type is not None:
        #     print(f"return_type: {self.return_type}")
        #     value.returns = ast.parse(self.return_type)
            # print(ast.dump(returns))

        if self.is_class_method:
            # @Mstep [] add the "self" argument to the method.
            value.args.args.insert(0,ast.arg(arg='self'))
            # @Mstep [] add the getter/setter decorators.
            if self.is_getter:
                value.decorator_list.append(ast.Name(
                    id='property',
                    ctx=ast.Load()
                    )
                )
            if self.is_setter:
                attr = ast.Attribute(
                            value=ast.Name(
                                id=self.name.name,
                                ctx=ast.Load()
                            ),
                            attr='setter',
                            ctx=ast.Load()
                        )
                value.decorator_list.append(attr)

        # print(f"self.arg_list: {len(self.arg_list)}")
        for arg in self.arg_list:
            value.args.args.append(arg.ast)

        # @Mstep [IF] if there are keyword arguments
        if len(self.kwarg_list) > 0:
            # @Mstep [] add the keyword argument variable to the method.
            value.args.kwarg = ast.arg(arg='kwargs')

        # @Mstep [] apply the body.
        value.body.append(ast.parse(self._body))

        # @Mstep [] prepend the docblock to the method body.
        # self.Doc.subject_name = self.name.name
        # self.Doc.description = self.description
        self.Doc = _docblock.ClassMethodDocBlock(self)
        self.Doc.indent = self.indent + 4
        value.body.insert(0,ast.Expr(value=ast.Constant(value=self.Doc.result)))



        value = ast.fix_missing_locations(value)
        return value


# def populate_from_dict(data:dict,instance:Method):
#     for k,v in data.items():
#         if hasattr(instance,k):
#             setattr(instance,k,v)


