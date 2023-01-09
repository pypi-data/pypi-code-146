# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import




from dataclasses import dataclass
import re
from string import Template
from typing import Iterable, Union
import ast

import colemen_utils as c
import silent.EntityBase as _eb


# import silent.Class.Method as _method
# from config import column_type,_relationship_type,endpointdoc_type,route_type,root_directory,susurrus_type
import silent.se_config as config
log = c.con.log


@dataclass
class Property(_eb.EntityBase):


    data_type:str = None
    '''The python data type that this property stores.'''

    default = None
    '''The default value to assign to this property'''


    is_private:bool = False
    '''True if this property is private to its class.'''

    getter_body:str = None
    '''The body of the getter method.'''

    indent:int = 4


    getter_method:config._method_type = None
    setter_method:config._method_type = None

    def __init__(self,main:config._main_type,pyClass:config._py_class_type,name:str,description:str=None,
                tags:Union[str,list]=None,data_type:str=None,default=None,private:bool=False,getter_body:str=None,
            ) -> None:
        '''
            Represents a class property.

            ----------

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
        kwargs['pyclass'] = pyClass
        kwargs['module'] = pyClass.module
        kwargs['name'] = name
        kwargs['description'] = description
        kwargs['tags'] = tags
        kwargs['data_type'] = data_type
        kwargs['default'] = default
        kwargs['private'] = private
        kwargs['getter_body'] = getter_body

        super().__init__(**kwargs)
        
        if isinstance(tags,(list)):
            self.add_tag(tags)

        if isinstance(self.default,(str)) and isinstance(self.data_type,(str)):
            if self.data_type in ["int","integer"]:
                self.data_type = "int"
                if c.valid.numeric_only(self.default):
                    self.default = int(self.default)









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
            "data_type":self.data_type,
            "default":self.default,
            "is_private":self.is_private,
            "tags":self._tags,
            # "schema":self.table.database.database,
        }

        return value



    def _gen_getter(self):
        pass



    @property
    def attribute_name(self):
        '''
            Get this Property's attribute_name

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 09:15:52
            `@memberOf`: Property
            `@property`: attribute_name
        '''
        value = self.name.name
        if self.is_private:
            value = f"_{self.name.name}"
        return value

    @property
    def attribute_type(self)->str:
        '''
            Get the attribute_type value.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-26-2022 12:10:46
            `@memberOf`: PostArg
            `@property`: attribute_type
        '''
        value = ""

        if isinstance(self.data_type,(str)):
            value = c.string.strip(self.data_type,":")
            value = f":{value}"
        return value

    @property
    def attribute_description(self):
        '''
            Get this Property's attribute_description

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-04-2023 11:11:47
            `@memberOf`: Property
            `@property`: attribute_description
        '''
        value = ""
        if isinstance(self.description,(str)):
            if len(self.description) > 0:
                value = c.string.strip(self.description,["'"])
                value = f"'''{value}'''"
        return value

    @property
    def default_value(self)->str:
        '''
            Get the default_value value.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-27-2022 10:25:55
            `@memberOf`: PostArg
            `@property`: default_value
        '''
        value = self.default
        if isinstance(value,(str)):
            value = c.string.strip(value,['"'])
            value = f'"{value}"'
        return value


    @property
    def getter(self)->config._method_type:
        '''
            Get this Property's getter

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-09-2023 16:21:26
            `@memberOf`: Property
            `@property`: getter
        '''
        if self.getter_method is not None:
            return self.getter_method

        # @Mstep [IF] if the class is a dataclass and the property is not private
        if self.pyclass.is_dataclass and self.is_private is False:
            # @Mstep [RETURN] return None, the dataclass will manage this property.
            return None

        mthd = self.pyclass.get_method(self.name,is_getter=True)
        if mthd is None:
            self.getter_method = self.pyclass.add_getter(self.name.name,prop=self)
        else:
            self.getter_method = mthd
        return self.getter_method

    @property
    def setter(self)->config._method_type:
        '''
            Get this Property's setter

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-09-2023 16:21:26
            `@memberOf`: Property
            `@property`: setter
        '''
        if self.setter_method is not None:
            return self.setter_method

        # @Mstep [IF] if the class is a dataclass and the property is not private
        if self.pyclass.is_dataclass and self.is_private is False:
            # @Mstep [RETURN] return None, the dataclass will manage this property.
            return None

        mthd = self.pyclass.get_method(self.name,is_setter=True)
        if mthd is None:
            self.setter_method = self.pyclass.add_setter(self.name.name,prop=self)
        else:
            self.setter_method = mthd
        return self.setter_method


    # @property
    # def getter(self):
    #     '''
    #         Generate this Property's getter method

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 01-04-2023 09:08:27
    #         `@memberOf`: Property
    #         `@property`: getter
    #     '''
    #     if self.pyclass.is_dataclass and self.is_private is False:
    #         return ""

    #     description = self.description
    #     if description is None or len(description) == 0:
    #         description = f"Retrieve the {self.name.name} property from {self.pyclass.name}"
    #     body = self.getter_body
    #     if body is None or len(body) == 0:
    #         body = f"        return self.{self.attribute_name}"

    #     method = self.pyclass.add_method(
    #         self.name.name,
    #         description=description,
    #         body=body,
    #         return_type=self.data_type,
    #         is_getter=True
    #     )
    #     return method

    # @property
    # def declaration(self):
    #     '''
    #         Get this Property's declaration

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 01-04-2023 09:17:47
    #         `@memberOf`: Property
    #         `@property`: declaration
    #     '''
    #     # import ast
    #     # ass = ast.AnnAssign(
    #     #     target=[
    #     #         ast.Name(
    #     #             id=self.attribute_name,
    #     #             ctx=ast.Store())
    #     #         ],
    #     #     annotation=ast.Name(id=self.attribute_type,ctx=ast.Load()),
    #     #     value=ast.Constant(
    #     #         value=self.default_value
    #     #     ),
    #     #     simple=1
    #     # )
    #     # value = ast.unparse(ass)
    #     # return " "*self.indent + value
    #     _ = self.getter
    #     s = Template(config.get_template("property_declaration_template"))
    #     value = s.substitute(
    #         attribute_name=self.attribute_name,
    #         attribute_type=self.attribute_type,
    #         default_value=self.default_value,
    #         description=self.attribute_description,
    #     )
    #     return value



    @property
    def declaration_ast(self)->Union[ast.Assign,ast.AnnAssign,ast.Expr]:
        '''
            Get this Property's declaration ast object

            If this property has a description a list will be returned:
            [assignment,description]

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 12:04:27
            `@memberOf`: Property
            `@property`: ast
        '''
        name = self.name.name
        if self.is_private:
            name = f"_{name}"

        if self.data_type is not None:
            value = ast.AnnAssign(
                target=ast.Name(id=name, ctx=ast.Store()),
                annotation=ast.Name(id='str', ctx=ast.Load()),
                value=ast.Constant(value=None),
                simple=1
            )
            if self.data_type is not None:
                value.annotation = ast.Name(id=self.data_type, ctx=ast.Load())
                # Expr(
                #     value=Constant(value='The method name'))
        else:
            value = ast.Assign(
                targets=[
                    ast.Name(id=name, ctx=ast.Store())
                    ],
                value=ast.Constant(value=None)
            )

        if self.default is not None:
            value.value = ast.Constant(value=self.default)

        if self.description is not None:
            description = ast.Expr(value=ast.Constant(value=self.description))
            value = [value,description]

        return value

    @property
    def declaration_result(self):
        '''
            Get this Property's declaration_result

            `default`:None

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 12:10:47
            `@memberOf`: Property
            `@property`: declaration_result
        '''
        value = self.declaration_ast
        if self.description is not None:
            description = ast.Expr(value=ast.Constant(value=self.description))
            value = [value,description]
        # value = ast.fix_missing_locations(value)
        
        return ast.unparse(value)

    
    def assign_ast(self,value,include_description=False):
        '''
            Get this Property's assign_ast

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 14:00:14
            `@memberOf`: Property
            `@property`: assign_ast
        '''
        assign = f"self.{self.attribute_name}{self.attribute_type} = {value}"
        if include_description is True:
            assign = f"{assign}\n'{self.description}'"
        value = ast.parse(assign)
        return value

    def assign_result(self,value,include_description=False):
        '''
            Get this Property's assign_ast

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 01-05-2023 14:00:14
            `@memberOf`: Property
            `@property`: assign_ast
        '''
        value = ast.unparse(self.assign_ast(value,include_description))
        return value
