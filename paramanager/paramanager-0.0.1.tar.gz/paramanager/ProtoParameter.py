from .Parameter import Parameter

ALLOWED_CHARS = [chr(i + 97) for i in range(26)] + [chr(i + 65) for i in range(26)] + ["_"]


def matches_allowed_chars(string: str):
    return all(c in ALLOWED_CHARS for c in string)


class ProtoParameter:
    def __init__(self, name: str, default_value, parser=float, pseudonyms : list[str] = []):
        self.name = name
        self.value = default_value
        self.parser = parser
        self.pseudonyms = pseudonyms + [name]

        if any(not matches_allowed_chars(name) for name in self.pseudonyms):
            raise ValueError("name or pseudonym contains illegal character (not letters or '_')")

    def __call__(self):
        return Parameter(self.name, self.value)

    def set_value(self, string):
        try:
            self.value = self.parser(string)
        except ValueError:
            print(f"ValueError when parsing '{string}' for '{self.name}'")
            return

    def names(self):
        return self.pseudonyms
