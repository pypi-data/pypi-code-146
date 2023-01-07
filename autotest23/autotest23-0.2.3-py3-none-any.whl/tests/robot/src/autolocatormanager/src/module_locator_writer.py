from typing import Any
from .abstract.i_module_locator_writer import IModuleLocatorWriter


class ModuleLocatorWriter(IModuleLocatorWriter):

    def module_code_writer(self, module_path: str, module_code: dict, is_override=None):
        locator_scope = "global"
        locator_access_modifier = "+"  # Public
        indentation = 4
        locator_collections = module_code
        code_body = self._declare_variables(locator_scope, locator_access_modifier, indentation, locator_collections)
        # Getting file text as line by line
        with open(module_path, "r") as in_file:
            buf = in_file.readlines()
        # Writing Codes in the targeted script
        if is_override == "y":
            try:
                new_code_body_list = self.code_body_str_to_list(code_body)
                old_code_body = buf[4:-4]
                updated_data = list()
                before = list(buf[:4])
                if len(old_code_body) > 0:
                    for var in new_code_body_list:
                        updated_data.append(self.update_old_code_body_data(var, old_code_body))
                    before.append("".join(updated_data))
                else:
                    # if old cody body not exist, add updated code body
                    if len(new_code_body_list) > 0:
                        before.append("".join(new_code_body_list))
                    else:
                        before = before
                buf = before + buf[-3:]
                with open(module_path, "w") as out_file:
                    for line in buf:
                        out_file.write(line)
                return f"File Path: {module_path}\n===> Module declaring locators as variables successful <==="
            except Exception as err:
                return f"File Path: {module_path} \n Error: {err}"
        else:
            try:
                with open(module_path, "w") as out_file:
                    """
                    split buf into two part, first part from 0 to 3 then append code body
                    and remove old variable from this buf list, and last part take -3 to last index
                    of buf list.
                    """
                    # `before` value stored till `class` declaration of ClassName.
                    before = list(buf[:4])
                    before.append(code_body)
                    buf = before + buf[-3:]
                    for line in buf:
                        out_file.write(line)
                return f"File Path: {module_path}\n===> Module declaring locators as variables successful <==="
            except Exception as err:
                return f"File Path: {module_path} \n Error: {err}"

    def code_body_str_to_list(self, _code_body: str) -> list:
        arr = list()
        for i in _code_body[1:-1].split("\n"):
            arr.append(i + "\n")
        return arr

    def update_old_code_body_data(self, _var: str, _old_body: list) -> str:
        """"""
        variable, value = _var.split("=")
        for element in _old_body:
            old_var, old_val = element.split("=")
            if variable.strip() == old_var.strip() and value.strip() == old_val.strip():
                return element
        return variable + "=" + value

    def _declare_variables(self, scope: str, variables_access_modifiers: str, indentation: int,
                           variables_collection: dict) -> str:
        code_body = """\n"""
        for locator in variables_collection:
            # Adding new line of code (declaring variables) and preparing the code body line by line.
            code_body += "" + self._declare_single_variable(indentation, locator, str,
                                                            variables_collection[locator]) + "\n"
        # Returning the updated code body. ///error occuring
        return code_body

    def _declare_single_variable(self, indentation: int, variable_name: str, variable_data_type: Any,
                                 variable_value: Any) -> str:
        locator_with_value = self.arrange_locator_by_type(variable_name, variable_value)
        new_line_code = " " * indentation + locator_with_value
        return new_line_code

    def arrange_locator_by_type(self, locators_name: str, locators_value: dict):
        # Converting a general string into a variable_name (Snake case - PEP8)
        locators_name = self._variable_name_converter(None, locators_name)
        # Getting the first key as locator type. Example: XPath, ID etc.
        locator_type = list(locators_value.keys())[0]
        # Converting the locator type name into a variable_name (Snake case - PEP8)
        locator_type_text = self._variable_name_converter(None, locator_type)
        # Preparing the final locator name as a Variable
        locators_name = f"{locators_name}_{locator_type_text}"
        # Getting the Data Type by the value.
        data_type = self._data_type_identifier_by_value(locators_value[locator_type])
        # Returning the locator variable declaration as a new line code.
        return f'{locators_name}: {data_type} = "{locators_value[locator_type]}"'

    def _variable_name_converter(self, variables_access_modifier: str, variable_name: str) -> str:
        # Replacing all white spaces with _
        variable = variable_name.replace(" ", "_")
        # Making the String lower case.
        variable = variable.lower()
        # Removing SpecialChars
        variable = variable.translate({ord(c): "_" for c in "!@#$%^&*()[]{;}:,./<>?\|`~-=+"})
        if variables_access_modifier == "+" or variables_access_modifier is None:  # Public
            pass
        elif variables_access_modifier == "-":  # Private
            variable = "__" + variable
        elif variables_access_modifier == "#":  # Protected
            variable = "_" + variable
        else:
            raise "Variable access modifier unknown!"
        # Returning converted string in Snake Case
        return variable

    def _data_type_identifier_by_value(self, variable_value: Any) -> Any:
        return type(variable_value).__name__
