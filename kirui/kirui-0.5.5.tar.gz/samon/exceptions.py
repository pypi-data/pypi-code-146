

class TemplateError(Exception):
    """Base class for all template errors."""
    pass


class TemplateNotFound(TemplateError):
    pass


class ElementNameConflict(Exception):
    def __init__(self, class_name: str):
        self.class_name = class_name

    def __str__(self):
        return 'Class conflict: {0}'.format(self.class_name)
