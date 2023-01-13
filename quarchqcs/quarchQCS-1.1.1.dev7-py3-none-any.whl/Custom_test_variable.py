# Add custom unit type, to avoid having to parse units out of strings under the hood?
# propose custom_name -> name, custom_value -> value, default_value -> default


class CustomVariable:
    def __init__(self, name, description="", default_value=0, var_purpose="user", custom_val=None, var_unit=None,
                 accepted_vals=None, numerical_max=None, type=False, file_path="", var_group="Test"):
        self.custom_name = name
        self.description = description
        self.default_value = default_value
        self.custom_value = default_value
        if custom_val:
            self.custom_value = custom_val
        self.var_purpose = var_purpose
        self.var_unit = var_unit
        self.acceptedVals = accepted_vals
        self.numerical_max = numerical_max
        self.type = type
        self.file_path=file_path
        self.var_group = var_group

    def _name_of_file_path_key(self):
        return self.custom_name + "__file_path"

    def reset_custom_value(self):
        self.custom_value = self.default_value

    def __str__(self):
        if self.var_unit:
            return str(self.custom_value) + self.var_unit
        else:
            return str(self.custom_value)
