from typing import Optional


class GenerationFile:
    def __init__(
        self, *, name: Optional[str] = None, template_name: Optional[str] = None, parameters: Optional[dict] = None
    ):
        if not any([name, template_name]):
            raise ValueError("Generation file must have name or template_name")
        self.name = name or ""
        self.template_name = template_name or ""
        self.parameters = parameters or {}

    def __eq__(self, other):
        if isinstance(other, GenerationFile):
            return (
                self.name == other.name
                and self.template_name == other.template_name
                and self.parameters == other.parameters
            )
        return False


class GenerationDirectory:
    nested = []

    def __init__(self, name: str, nested=None):
        self.name = name
        self.nested = nested or []

    def __eq__(self, other):
        if isinstance(other, GenerationDirectory):
            return self.name == other.name and all(
                [self_nested == other_nested for self_nested, other_nested in zip(self.nested, other.nested)]
            )
        return False
