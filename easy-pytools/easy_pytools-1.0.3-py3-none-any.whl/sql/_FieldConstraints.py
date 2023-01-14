class FieldConstraint:
    """Field constraint base class"""
    name = ""

    def __init__(self, *args):
        self.details = [str(a) for a in args]

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'{self.name}({",".join(self.details)})'

    def __hash__(self):
        return hash((self.name, self.details))

    def __eq__(self, other: 'FieldConstraint'):
        return hash(self) == hash(other)


class NotNull(FieldConstraint):
    """Not NULL constraint"""
    name = "NOTNULL"


class Primary(FieldConstraint):
    """Primary key constraint"""
    name = "PRIMARY"


class Foreign(FieldConstraint):
    """Foreign key constraint"""
    name = "FOREIGN"


class Check(FieldConstraint):
    name = "CHECK"


class Unique(FieldConstraint):
    name = "UNIQUE"


class Default(FieldConstraint):
    name = "DEFAULT"