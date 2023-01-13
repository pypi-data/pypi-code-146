import re
import collections


class SemVer:
    """
    semantic versioning class

    => see https://semver.org
    """
    def __init__(
        self,
        major: int = 0,
        minor: int = 0,
        patch: str = 0,
        prerelease: str = None,
        buildmetadata: str = None
    ):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.prerelease = prerelease
        self.buildmetadata = buildmetadata

    @property
    def major(self) -> int:
        """
        major part of the version

        :return: major part of the version
        :rtype: int
        """
        return self._major

    @major.setter
    def major(self, value: int):
        """
        set major part of the version

        :param value: major part of the version
        :type value: int
        """
        assert isinstance(value, int) and (value >= 0)

        self._major = value

    @property
    def minor(self) -> int:
        """
        minor part of the version

        :return: minor part of the version
        :rtype: int
        """
        return self._minor

    @minor.setter
    def minor(self, value: int):
        """
        set minor part of the version

        :param value: minor part of the version
        :type value: int
        """
        assert isinstance(value, int) and (value >= 0)

        self._minor = value

    @property
    def patch(self) -> int:
        """
        patch part of the version

        :return: patch part of the version
        :rtype: int
        """
        return self._patch

    @patch.setter
    def patch(self, value: int):
        """
        set patch part of the version

        :param value: patch part of the version
        :type value: str
        """
        assert isinstance(value, int) and (value >= 0)

        self._patch = value

    @property
    def prerelease(self) -> str:
        """
        prerelease part of the version

        :return: prerelease part of the version
        :rtype: str
        """
        return self._prerelease

    @prerelease.setter
    def prerelease(self, value: str):
        """
        set prerelease part of the version

        :param value: prerelease part of the version
        :type value: str
        """
        assert (value is None) or isinstance(value, str)

        self._prerelease = value

    @property
    def buildmetadata(self) -> str:
        """
        buildmetadata part of the version

        :return: buildmetadata part of the version
        :rtype: str
        """
        return self._buildmetadata

    @buildmetadata.setter
    def buildmetadata(self, value: str):
        """
        set buildmetadata part of the version

        :param value: buildmetadata part of the version
        :type value: str
        """
        assert (value is None) or isinstance(value, str)

        self._buildmetadata = value

    @staticmethod
    def create_from_str(s: str) -> "SemVer":
        """
        create SemVer class instance from given string

        :param s: input string from which SemVer class instance should be built
        :type value: str
        :return: SemVer class instance based on given string
        :rtype: SemVer
        :raises TypeError: if incorrect string input
        """
        assert isinstance(s, str)

        res = re.compile(
            r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|"
            r"[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-]"
            r"[0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*)"
            r")?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
        ).match(s)
        if not res:
            # not a valid SemVer
            raise TypeError(f"The string '{s}' is not a valid SemVer.")

        # get group dict
        d = res.groupdict()

        # convert to integer values
        for field in ("major", "minor", "patch"):
            d[field] = int(d[field])

        return SemVer(**d)

    def __str__(self) -> str:
        """
        string representation of SemVer class

        :return: string representation of SemVer class
        :rtype: str
        """
        tmp = f"{self.major}.{self.minor}"
        if self.patch is not None:
            tmp += f".{self.patch}"
        if self.prerelease is not None:
            tmp += f"-{self.prerelease}"
        if self.buildmetadata is not None:
            tmp += f"+{self.buildmetadata}"

        return tmp

    def __repr__(self) -> str:
        """
        string representation of SemVer class

        :return: string representation of SemVer class
        :rtype: str
        """
        return (
            f"<SemVer(major={self.major}, "
            f"minor={self.minor}, "
            f"patch={self.patch}, "
            f"prerelease={self.prerelease}, "
            f"buildmetadata={self.buildmetadata})>"
        )
