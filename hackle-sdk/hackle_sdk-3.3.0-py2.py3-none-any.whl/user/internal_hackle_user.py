class InternalHackleUser(object):
    def __init__(self, identifiers, properties):
        self.identifiers = identifiers
        self.properties = properties

    def __eq__(self, other):
        if not isinstance(other, InternalHackleUser):
            return False
        return self.identifiers == other.identifiers and self.properties == other.properties

    def __ne__(self, other):
        return not self.__eq__(other)
