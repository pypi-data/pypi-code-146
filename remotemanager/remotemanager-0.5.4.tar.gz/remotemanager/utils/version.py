class Version:
    """
    Lightweight temporary class for version comparison.

    Create at least one instance of Version to compare two semantic versions:

    >>> v = Version('1.5.2')
    >>> v < '4.1.0'
    >>> True

    Args:
        ver (str):
            Semantic version in x.y.z form
    """

    def __init__(self, ver):

        self._version = ver

        self._major, self._minor, self._patch = \
            [int(v) for v in ver.split('.')]

    def __eq__(self, other):
        if not isinstance(other, Version):
            other = Version(other)

        return all([self.major == other.major,
                    self.minor == other.minor,
                    self.patch == other.patch])

    def __lt__(self, other):
        if not isinstance(other, Version):
            other = Version(other)

        if self.major == other.major:
            if self.minor == other.minor:
                if self.patch == other.patch:
                    return False
                return self.patch < other.patch
            return self.minor < other.minor
        return self.major < other.major

    def __gt__(self, other):
        if not isinstance(other, Version):
            other = Version(other)

        if self.major == other.major:
            if self.minor == other.minor:
                if self.patch == other.patch:
                    return False
                return self.patch > other.patch
            return self.minor > other.minor
        return self.major > other.major

    def __le__(self, other):
        if not isinstance(other, Version):
            other = Version(other)

        return self == other or self < other

    def __ge__(self, other):
        if not isinstance(other, Version):
            other = Version(other)

        return self == other or self > other

    def __repr__(self):
        return f'{self.major}.{self.minor}.{self.patch}'

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def patch(self):
        return self._patch

    @property
    def version(self):
        return self._version
