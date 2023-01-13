# Base exception class for all SubGit related exceptions
class SubGitException(Exception):
    pass


# Exceptions that is realted to the ".subgit.yml" config file and the contents in it
class SubGitConfigException(SubGitException):
    pass


# Exceptions that happen related to some error with the git repo itself when
# we attempt to make an operation on it.
class SubGitRepoException(SubGitException):
    pass


__all__ = [
    "SubGitException",
    "SubGitConfigException",
    "SubGitRepoException",
]
