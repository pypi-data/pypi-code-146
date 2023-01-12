"""
This module contains domain models for meta data.
"""


class MetaProperty:
    """
    This class contains the model for a meta property.
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.value = kwargs.get("value")

    @property
    def name(self):
        """
        Returns the name of the property.
        """
        return self._name

    @name.setter
    def name(self, input_name: str):
        """
        Sets the name of the property.
        """
        if input_name is not None:
            input_name = input_name.strip()

        self._name = input_name

    @property
    def value(self):
        """
        Returns the value of the property.
        """
        return self._value

    @value.setter
    def value(self, input_value):
        """
        Sets the value of the property.
        """
        if input_value is not None:
            if not isinstance(input_value, str):
                input_value = str(input_value)
                input_value = input_value.strip()

        self._value = input_value

    def __repr__(self):
        """
        Returns a string representation of the object.
        """
        if self.value is None:
            return f"{self.name}=null"

        return f"{self.name}='{self.value}'"

    def __eq__(self, other):
        """
        Returns true if the two objects are equal.
        """
        return self.name == other.name and self.value == other.value


class MetaModel:
    """
    This class contains the domain model for meta data.
    """

    def __init__(self, **kwargs):
        self.meta = kwargs.get("meta", [])

    def has_property(self, name: str) -> bool:
        """
        This method checks if a property exists in the meta data.
        """
        for item in self.meta:
            if item.name == name:
                return item.value is not None and item.value != ""

        return False

    def get_property(self, name: str):
        """
        This method returns the value of a property.
        """
        for item in self.meta:
            if item.name == name:
                return item.value

        return None

    def update_property(self, name: str, value: str):
        """
        This method updates a property in the meta data.
        """
        found = False
        for item in self.meta:
            if item.name == name:
                found = True
                item.value = value

        if not found:
            self.add_property(name, value)

    def add_property(self, name: str, value: str):
        """
        This method adds a property to the meta data.
        """
        if value is not None:

            if isinstance(value, str):
                value = value.strip()

                if len(value) == 0:
                    value = None

        if self.has_property(name):
            self.update_property(name, value)
        else:
            self.meta.append(MetaProperty(name=name, value=value))

    def remove_property(self, name: str):
        """
        This method removes a property from the meta data.
        """
        for item in self.meta:
            if item.name == name:
                self.meta.remove(item)
                break
