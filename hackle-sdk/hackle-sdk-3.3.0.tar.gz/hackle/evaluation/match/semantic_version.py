import re

from six import string_types


def compare_values(a, b):
    return (a > b) - (a < b)


def compare_identifiers(identifier1, identifier2):
    if identifier1.isnumeric() and identifier2.isnumeric():
        return compare_values(int(identifier1), int(identifier2))
    else:
        return compare_values(identifier1, identifier2)


class SemanticVersion(object):
    _REGEX = re.compile(
        r"""
            ^(0|[1-9]\d*)
            (?:\.(0|[1-9]\d*))?
            (?:\.(0|[1-9]\d*))?
            (?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?
            (?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?
            $
        """,
        re.VERBOSE,
    )

    def __init__(self, core_version, prerelease, build):
        self.core_version = core_version
        self.prerelease = prerelease
        self.build = build

    def compare(self, other):
        result = self.core_version.compare(other.core_version)
        if result != 0:
            return result
        else:
            return self.prerelease.compare(other.prerelease)

    def __str__(self):
        version = str(self.core_version)
        if self.prerelease.is_not_empty():
            version += "-{}".format(self.prerelease)
        if self.build.is_not_empty():
            version += "+{}".format(self.build)
        return version

    def __eq__(self, other):
        return self.compare(other) == 0

    def __ne__(self, other):
        return self.compare(other) != 0

    def __gt__(self, other):
        return self.compare(other) > 0

    def __ge__(self, other):
        return self.compare(other) >= 0

    def __le__(self, other):
        return self.compare(other) <= 0

    def __lt__(self, other):
        return self.compare(other) < 0

    @staticmethod
    def parse_or_none(value):
        if not isinstance(value, string_types):
            return None

        match = SemanticVersion._REGEX.match(value)
        if match is None:
            return None

        groups = match.groups()

        major = groups[0]
        minor = groups[1]
        patch = groups[2]

        core_version = CoreVersion(
            major=int(major),
            minor=int(minor) if minor is not None else 0,
            patch=int(patch) if patch is not None else 0,
        )
        prerelease = MetadataVersion.parse(groups[3])
        build = MetadataVersion.parse(groups[4])

        return SemanticVersion(core_version, prerelease, build)


class CoreVersion(object):

    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def compare(self, other):
        a = (self.major, self.minor, self.patch)
        b = (other.major, other.minor, other.patch)
        return compare_values(a, b)

    def __str__(self):
        return "{}.{}.{}".format(self.major, self.minor, self.patch)


class MetadataVersion(object):

    def __init__(self, identifiers):
        self.identifiers = identifiers

    def is_empty(self):
        return len(self.identifiers) == 0

    def is_not_empty(self):
        return not self.is_empty()

    def compare(self, other):
        if self.is_empty() and other.is_empty():
            return 0

        if self.is_empty() and other.is_not_empty():
            return 1

        if self.is_not_empty() and other.is_empty():
            return -1

        return self.compare_identifiers(other)

    def compare_identifiers(self, other):
        for self_identifier, other_identifier in zip(self.identifiers, other.identifiers):
            result = compare_identifiers(self_identifier, other_identifier)
            if result != 0:
                return result
        else:
            return compare_values(len(self.identifiers), len(other.identifiers))

    def __str__(self):
        return ".".join(self.identifiers)

    @staticmethod
    def parse(value):
        if value is None:
            return MetadataVersion([])
        else:
            return MetadataVersion(value.split("."))
