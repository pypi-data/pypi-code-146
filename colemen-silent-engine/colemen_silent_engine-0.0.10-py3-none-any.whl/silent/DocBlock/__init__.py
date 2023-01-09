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


@dataclass
class DocBlock:

    return_type:str = None
    '''The datatype returned by this'''
    subject_name:str = None
    '''The name of the subject of this docblock'''
    description:str = None
    '''The description of the docblock'''
    return_description:str = None
    return_type:str = None
    indent:str = 4
    _member_of:str = None

    _arguments=None
    '''A list of argument strings'''


    def __init__(self,data:dict = None) -> None:
        self._arguments = []
        if data is not None:
            if isinstance(data,(dict)):
                for k,v in data.items():
                    if hasattr(self,k):
                        setattr(self,k,v)

    def add_argument(self,name,data_type,description,default="__NO_DEFAULT_PROVIDED__"):
        s = Template(config.get_template("docblock_single_arg"))

        name = f"`{name}`"
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
        value = ''
        if len(self._arguments) > 0:
            args = '\n\n'.join(self._arguments)
            value = f'''Arguments\n    -------------------------\n{args}'''
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

        s = Template(config.get_template("docblock_template"))
        value = s.substitute(
            description=self.description,
            subject_name=self.subject_name,
            member_of=self.member_of,
            timestamp=datetime.datetime.today().strftime("%m-%d-%Y %H:%M:%S"),
            arguments=self.arguments,
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
        # value = re.sub(r"^\s*$","\n",value,re.MULTILINE)
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





