class AStringHaving(str):
    def __eq__(self, other):
        return self in other
