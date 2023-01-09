# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import




import os
import re
import datetime
from dataclasses import dataclass
from typing import Iterable
import colemen_utils as c
from string import Template

import silent.se_config as config
log = c.con.log


SINGLE_ARG_TEMPLATE='''    $name {$data_type}
        $description'''

DOCBLOCK_TEMPLATE = '''    $description

    $arguments

    $kwargs

    $returns

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: $timestamp
    `version`: 1.0
    `method_name`: $subject_name
    * @xxx [$timestamp]: documentation for $subject_name'''

@dataclass
class ClassMethodDocBlock:

    pyclass:config._py_class_type = None
    '''A reference to the class that the method belongs to.'''
    class_prop:config._py_property_type = None
    '''A reference to the class property that the method manages. (if it is a getter or setter)'''
    
    return_type:str = None
    '''The datatype returned by this'''
    subject_name:str = None
    '''The name of the subject of this docblock'''
    description:str = None
    '''The description of the docblock'''
    return_description:str = None
    return_type:str = None
    indent:int = 4
    _member_of:str = None

    _arguments=None
    '''A list of argument strings'''
    _kwargs=None


    def __init__(self,classMethod:config._method_type,data:dict = None) -> None:
        self._arguments = []
        self._kwargs = []
        self.classMethod = classMethod
        if data is not None:
            if isinstance(data,(dict)):
                for k,v in data.items():
                    if hasattr(self,k):
                        setattr(self,k,v)

        self.pyclass = self.classMethod.pyclass
        # if hasattr(self.classMethod,'name'):
        self.subject_name = self.classMethod.name.name
        if self.classMethod.name.name == "__init__":
            self.subject_name = self.classMethod.pyclass.name.name
            self.description = self.classMethod.pyclass.description

        if hasattr(self.classMethod,'description'):
            self.description = self.classMethod.description

        self.return_type = self.classMethod.return_type
        self.return_description = self.classMethod.return_description

        if self.classMethod.is_setter or self.classMethod.is_getter:
            self.class_prop = self.pyclass.get_property(self.subject_name)
            if self.class_prop is not None:
                self.return_description = self.class_prop.description







    def add_argument(self,name,data_type,description,default="__NO_DEFAULT_PROVIDED__"):
        s = Template(SINGLE_ARG_TEMPLATE)

        name = f"`{name}`"
        if data_type is None:
            data_type = "any"
        if default != "__NO_DEFAULT_PROVIDED__":
            if isinstance(default,(str)):
                default = f"'{default}'"
            name = f"[{name}={default}]"

        value = s.substitute(
            name=name,
            data_type=data_type,
            description=description,
        )
        self._arguments.append(value)


    def add_kwarg(self,name,data_type,description,default="__NO_DEFAULT_PROVIDED__"):
        s = Template(SINGLE_ARG_TEMPLATE)

        name = f"`{name}`"
        if data_type is None:
            data_type = "any"

        if default != "__NO_DEFAULT_PROVIDED__":
            if isinstance(default,(str)):
                default = f"'{default}'"
            name = f"[{name}={default}]"

        value = s.substitute(
            name=name,
            data_type=data_type,
            description=description,
        )
        self._kwargs.append(value)

    @property
    def arguments(self):
        '''
            Get the arguments property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-15-2022 10:55:22
            `@memberOf`: __init__
            `@property`: arguments
        '''
        self._arguments = []
        value = ''
        for arg in self.classMethod.arg_list:
            if arg.name.name.startswith("**"):
                continue
            self.add_argument(arg.name.name,arg.data_type,arg.description,arg.default)
            args = '\n\n'.join(self._arguments)
            value = f'''Arguments\n    -------------------------\n{args}'''
        return value

    @property
    def kwargs(self):
        '''
            Get the kwargs property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-15-2022 10:55:22
            `@memberOf`: __init__
            `@property`: kwargs
        '''
        self._kwargs = []
        value = ''
        for arg in self.classMethod.kwarg_list:
            self.add_kwarg(arg.name.name,arg.data_type,arg.description,arg.default)
            args = '\n\n'.join(self._kwargs)
            value = f'''Keyword Arguments\n    -------------------------\n{args}'''
        return value


    @property
    def member_of(self)->str:
        '''
            Get the member_of value.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-15-2022 11:04:10
            `@memberOf`: PostArg
            `@property`: member_of
        '''
        if self._member_of is None:
            return ""
        value = f"`memberOf`: {self._member_of}"
        return value

    @member_of.setter
    def member_of(self,value:str):
        '''
            Set the member_of value.

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-15-2022 11:04:10
            `@memberOf`: PostArg
            `@property`: member_of
        '''
        self._member_of = value


    @property
    def returns(self):
        '''
            Get the returns property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-15-2022 11:00:08
            `@memberOf`: __init__
            `@property`: returns
        '''
        if self.return_type is None and self.return_description is None:
            return ""
        value = f'''Return {{{self.return_type}}}
    ----------------------
    {self.return_description}
'''
        # value = self.returns
        return value


    @property
    def result(self):
        '''
            Get the result property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-08-2022 12:22:06
            `@memberOf`: __init__
            `@property`: result
        '''

        s = Template(DOCBLOCK_TEMPLATE)
        value = s.substitute(
            description=self.description,
            subject_name=self.subject_name,
            member_of=self.member_of,
            timestamp=datetime.datetime.today().strftime("%m-%d-%Y %H:%M:%S"),
            arguments=self.arguments,
            kwargs=self.kwargs,
            returns=self.returns,
        )
        vl = value.split("\n")
        indented = []
        # vl2 = []
        instring = " "*self.indent
        for l in vl:
            if len(c.string.strip(l,[" "])) == 0:
                indented.append("\n")
            else:
                indent = f"\n{instring}"
                indented.append(f"{indent}{l}")
        # vl = vl2
        value = "".join(indented)
        value = re.sub(r"[\s\n]*Meta","\n\n            Meta",value)
        value = re.sub(r"[\s\n]*Keyword",":\n\n            Keyword",value)
        value = re.sub(r"[\s\n]*Return",":\n\n            Return",value)
        if self.classMethod.is_class_method is False:
            value = value.replace("            Return","        Return")
            value = value.replace("            Meta","        Meta")
        # value = re.sub(r":[\s\n]*'''",":\n        '''",value)
        return value


# if __name__ == '__main__':
#     d = DocBlock()
#     d.description = "Some Description"
#     d.subject_name = "boobs"
#     d.add_argument("titties","nips","The titties and the nips")
#     d.add_argument("boobies","butts","The boobies and the butts","pussyFist")
#     # d.member_of = "ass"
#     d.return_type = "str"
#     d.return_description = "That stuff from the thing"
#     print(f"d.result")
#     print(d.result)





