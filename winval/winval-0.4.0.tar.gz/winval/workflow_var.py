from enum import Enum, auto
from winval import logger
from typing import Optional


class WorkflowVarType(Enum):
    STRING = auto()
    INT = auto()
    FLOAT = auto()
    FILE = auto()
    BOOLEAN = auto()
    STRING_ARRAY = auto()
    INT_ARRAY = auto()
    FLOAT_ARRAY = auto()
    FILE_ARRAY = auto()
    BOOLEAN_ARRAY = auto()
    FILE_MATRIX = auto()
    STRUCT = auto()

    @staticmethod
    def from_string(string: str):
        if string == 'String':
            return WorkflowVarType.STRING
        elif string == 'Int':
            return WorkflowVarType.INT
        elif string == 'Float':
            return WorkflowVarType.FLOAT
        elif string == 'File':
            return WorkflowVarType.FILE
        elif string == 'Boolean':
            return WorkflowVarType.BOOLEAN
        elif string == 'Array[String]':
            return WorkflowVarType.STRING_ARRAY
        elif string == 'Array[Int]':
            return WorkflowVarType.INT_ARRAY
        elif string == 'Array[Float]':
            return WorkflowVarType.FLOAT_ARRAY
        elif string == 'Array[File]':
            return WorkflowVarType.FILE_ARRAY
        elif string == 'Array[Boolean]':
            return WorkflowVarType.BOOLEAN_ARRAY
        elif string == 'Array[Array[File]]':
            return WorkflowVarType.FILE_MATRIX
        else:
            raise ValueError(f'No such WorkflowVarType: {string}')


class WorkflowVar:

    def __init__(self, name: str,
                 var_type: WorkflowVarType,
                 is_optional: bool,
                 default_value: Optional[str],
                 workflow_name: str,
                 struct_id: str = None):
        self.name = name
        self.type = var_type
        self.is_optional = is_optional
        self.value = self.__parse_default_value_from_str(default_value)
        self.workflow_name = workflow_name
        self.full_name = f'{workflow_name}.{name}'
        self.struct_id = struct_id

    def __repr__(self):
        is_opt = '?' if self.is_optional else ''
        return f'{self.name} {self.type} {is_opt} {self.value}'

    def set_value(self, value):
        self.value = value

    def __parse_default_value_from_str(self, value: str):
        if value is None:
            return None
        if self.type == WorkflowVarType.INT:
            try:
                return int(value)
            except ValueError:
                logger.warning(f'Ignore parsing complex default int expression {value}')
                return None
        if self.type == WorkflowVarType.FLOAT:
            try:
                return float(value)
            except ValueError:
                logger.warning(f'Ignore parsing complex default int expression {value}')
                return None

        if self.type == WorkflowVarType.BOOLEAN:
            if value == 'true':
                return True
            elif value == "false":
                return False
            else:
                logger.warning(f'Ignore parsing complex default bool expression {value}')
                return None
        if self.type in {WorkflowVarType.STRING_ARRAY,
                         WorkflowVarType.FILE_ARRAY,
                         WorkflowVarType.INT_ARRAY,
                         WorkflowVarType.BOOLEAN_ARRAY}:
            if value[0] not in {'['}:
                logger.warning(f'Ignore parsing complex default array value {value}')
                return None
            if value == '[]':
                return []
            else:
                str_array = value.strip('][ ').split(',')
                if self.type == WorkflowVarType.INT_ARRAY:
                    return [int(x) for x in str_array]
                if self.type == WorkflowVarType.FLOAT_ARRAY:
                    return [float(x) for x in str_array]
                if self.type == WorkflowVarType.BOOLEAN_ARRAY:
                    return [x == 'true' for x in str_array]
                else:
                    return [x.strip().strip('"').strip("'") for x in str_array]
        return value


