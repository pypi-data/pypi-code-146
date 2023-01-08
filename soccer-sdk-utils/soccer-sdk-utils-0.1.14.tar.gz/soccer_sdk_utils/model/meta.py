class MetaProperty:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.value = kwargs.get("value")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, input_name: str):
        if input_name is not None:
            input_name = input_name.strip()

        self._name = input_name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, input_value: str):
        if input_value is not None:
            if type(input_value) != str:
                input_value = str(input_value)

            input_value = input_value.strip()

        self._value = input_value

    def __repr__(self):
        if self.value is None:
            return f"{self.name}=null"
        else:
            return f"{self.name}='{self.value}'"
