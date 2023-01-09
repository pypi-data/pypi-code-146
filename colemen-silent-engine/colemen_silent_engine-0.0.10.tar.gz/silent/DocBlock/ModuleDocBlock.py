# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import




import os
import re
import datetime
from dataclasses import dataclass
from typing import Iterable
import silent.EntityBase as _eb
import colemen_utils as c
from string import Template

import silent.se_config as config
log = c.con.log


DOCBLOCK_TEMPLATE='''    $description

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: $timestamp
    `version`: 1.0
    `module_name`: $subject_name
    `member_of`: $package_name
    * @xxx [$timestamp]: documentation for $subject_name
'''


@dataclass
class ModuleDocBlock(_eb.EntityBase):
    indent:int = 0

    def __init__(self,main:config._main_type,module:config._py_module_type,**kwargs):
        '''
            Create a new module docblock.

            ----------

            Arguments
            -------------------------
            `main` {_main_type}
                A reference to the project instance

            `module` {Module}
                A reference to the Module instance

            Keyword Arguments
            -------------------------
            [`name`=None] {str}
                The name of the module.
                This will default to the module's actual name.

            [`description`=None] {str}
                The description of the module
                This will default to the module's description.

            [`indent`=0] {int}
                The indentation to apply the docblock

            Return {type}
            ----------------------
            return_description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-06-2023 11:10:11
            `memberOf`: ModuleDocBlock
            `version`: 1.0
            `method_name`: ModuleDocBlock
            * @xxx [01-06-2023 11:21:10]: documentation for ModuleDocBlock
        '''
        kwargs['main'] = main
        kwargs['module'] = module
        super().__init__(**kwargs)

        if self.name is None:
            self.name = self.module.name.name
        if self.description is None:
            self.description = self.module.description


    @property
    def result(self):
        '''
            Generate the documentation block string.

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
            subject_name=self.name.name,
            package_name=self.module.package.name.name,
            timestamp=datetime.datetime.today().strftime("%m-%d-%Y %H:%M:%S"),
        )
        vl = value.split("\n")
        indented = []
        instring = " "*self.indent
        for l in vl:
            if len(c.string.strip(l,[" "])) == 0:
                indented.append("\n")
            else:
                indent = f"\n{instring}"
                indented.append(f"{indent}{l}")
        value = "".join(indented)
        return value

