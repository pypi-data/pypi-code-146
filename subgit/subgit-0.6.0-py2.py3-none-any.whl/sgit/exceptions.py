# Base exception class for all Sgit related exceptions
class SgitException(Exception):
    pass


# Exceptions that is realted to the ".sgit.yml" config file and the contents in it
class SgitConfigException(SgitException):
    pass


# Exceptions that happen related to some error with the git repo itself when
# we attempt to make an operation on it.
class SgitRepoException(SgitException):
    pass


__all__ = [
    "SgitException",
    "SgitConfigException",
    "SgitRepoException",
]
