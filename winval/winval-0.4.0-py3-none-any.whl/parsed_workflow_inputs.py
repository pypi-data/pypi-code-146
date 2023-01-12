from __future__ import annotations
from winval.workflow_var import WorkflowVar, WorkflowVarType


class ParsedWorkflowInputs:
    """
    Stores workflow vars and name-space structs
    Fills values of variables from json inputs configuration
    """

    def __init__(self,
                 workflow_vars: dict[str, WorkflowVar],
                 structs: dict[str, dict[str, WorkflowVar]]):
        self.workflow_vars = workflow_vars
        self.structs = structs

    def fill_values_from_json(self, json_dict: dict):
        for var in self.workflow_vars.values():
            if var.full_name in json_dict:
                var.set_value(json_dict[var.full_name])
                if var.type == WorkflowVarType.STRUCT:
                    self.__validate_struct_assignment(var)
            else:
                if not var.is_optional and var.value is None:
                    raise ValueError(f'Mandatory input {var} is not set')

        for json_key in json_dict.keys():
            simple_name = json_key.split('.')[-1]
            if simple_name not in self.workflow_vars:
                raise ValueError(f'Variable {json_key} is not defined in workflow')

    def __validate_struct_assignment(self, struct_variable: WorkflowVar):
        struct_fields = self.structs[struct_variable.struct_id]
        field_values_dict = struct_variable.value
        for struct_field in struct_fields.values():
            if not struct_field.is_optional and struct_field.name not in field_values_dict:
                raise ValueError(f'Struct field {struct_field} is not set for used struct {struct_variable}')
        for json_struct_field in field_values_dict.keys():
            if json_struct_field not in struct_fields:
                raise ValueError(f'Field {json_struct_field} is not defined for struct {struct_variable.struct_id}')

