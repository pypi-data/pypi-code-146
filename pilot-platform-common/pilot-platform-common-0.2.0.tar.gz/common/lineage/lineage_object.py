# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import copy
import time


class LineageAttirbute:
    """The class is for Altas Lineage representation."""

    createTime: int
    updateTime: int
    qualifiedName: str
    name: str
    description: str
    inputs: list
    outputs: list

    def __init__(
        self, name: str, input_type: str, input_id: str, output_type: str, output_id: str, description: str
    ) -> None:

        self.qualifiedName = name
        self.name = name
        self.inputs = [{'typeName': input_type, 'uniqueAttributes': {'item_id': input_id}}]
        self.outputs = [{'typeName': output_type, 'uniqueAttributes': {'item_id': output_id}}]

        # default attirbutes
        cur_time = time.time()
        self.createTime = cur_time
        self.updateTime = cur_time
        self.description = description

    def json(self):
        return self.__dict__

class Lineage:
    typeName: str
    attributes: LineageAttirbute

    def __init__(self, typeName: str, attributes: LineageAttirbute):
        self.typeName = typeName
        self.attributes = copy.deepcopy(attributes)

    def json(self):
        res = {}
        for key, val in self.__dict__.items():
            if isinstance(val, str) or isinstance(val, int):
                res.update({key: val})
            # if we have sub class type, using the json()
            # function to format the return
            else:
                res.update({key: val.json()})

        return res
