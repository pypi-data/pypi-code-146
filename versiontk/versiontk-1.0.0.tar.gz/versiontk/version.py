from .objects import Version as __Version


def __str2version(__version: str):
    if "." in __version:
        parts = __version.split(".", 1)
        major = parts[0]
        minor = parts[1]
        if "." in minor:
            parts = minor.split(".", 1)
            minor = parts[0]
            patch = parts[1]
        else:
            patch = 0

    else:
        major, minor, patch = 1, 0, 0
    version = __Version(major=major, minor=minor, patch=patch)
    return version


def __upgrade_version(__v: __Version, __limit: int):
    if __v.patch < __limit:
        __v.patch += 1
    elif __v.minor < __limit:
        __v.minor += 1
        __v.patch = 0
    elif __v.major < __limit:
        __v.major += 1
        __v.minor = 0
        __v.patch = 0
    return __v


def __downgrade_version(__v: __Version, __limit: int):
    if __v.patch > 0:
        __v.patch -= 1
    elif __v.minor > 0:
        __v.minor -= 1
        __v.patch = __limit
    elif __v.major > 1:
        __v.major -= 1
        __v.minor = __limit
        __v.patch = __limit
    return __v


def __upgrade(version, limit: int):
    if isinstance(version, str):
        version = __str2version(version)
    return __upgrade_version(version, limit)


def __downgrade(version, limit: int):
    if isinstance(version, str):
        version = __str2version(version)
    return __downgrade_version(version, limit)


def __versions(__v: __Version):
    major = __v.major
    minor = __v.minor
    patch = __v.patch
    return f"{major}.{minor}.{patch}"


def upgrade(__version, limit: int):
    version = __upgrade(__version, limit)
    return __versions(version)


def downgrade(__version, limit: int):
    version = __downgrade(__version, limit)
    return __versions(version)
