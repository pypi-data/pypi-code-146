"""
Semantic versioning handler.

SPDX-License-Identifier: GPL-3.0-or-later
"""


class Semver:
    """Semantic versioning handling."""

    def __init__(self, slug: str):
        self.patch: int = 0
        versions = slug.split(".")
        slug_count = len(versions)
        if slug_count > 3 or slug_count < 2:
            raise ValueError(f"A version should have format X.Y[.Z], got {slug}")
        self.major: int = int(versions[0])
        self.minor: int = int(versions[1])
        if slug_count == 3:
            self.patch = int(versions[2])

    def is_compatible(self, other: "Semver") -> bool:
        """Are the two versions compatible?"""
        return self.major == other.major and self.minor == other.minor

    def __eq__(self, other) -> bool:
        if not isinstance(other, Semver):
            return False
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch

    def __gt__(self, other: "Semver") -> bool:
        """Magic method."""
        # If major and minor are equal, then check if patch is larger than
        # the other module.
        if self.major == other.major:
            if self.minor == other.minor:
                return self.patch > other.patch
            return self.minor > other.minor
        return self.major > other.major

    def __lt__(self, other: "Semver") -> bool:
        return other.__gt__(self)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
