"""The sole configuration option for conventionalish is the list of questions.

:author: Shay Hill
:created: 2023-01-09
"""

from commitizen.defaults import MAJOR, MINOR, PATCH

# fmt: off
# add or subtract questions here: (prefix, name, key, semver)
# semver is [MINOR, PATCH, or None], *not* MAJOR. MAJOR is always identified with
# "BREAKING CHANGE".
QUESTIONS = [
    ("fix", "A bug fix", "x", PATCH),
    ("feat", "A new feature", "f", MINOR),
    ("docs", "Documentation only changes", "d", None),
    ("style", "Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.)", "s", None),
    ("refactor", "A code change that neither fixes a bug nor adds a feature", "r", PATCH),
    ("perf", "A code change that improves performance", "p", PATCH),
    ("test", "Adding missing or correcting existing tests", "t", None),
    ("build", "Changes that affect the build system or external dependencies (example scopes: pip, docker, npm)", "b", None),
    ("ci", "Changes to our CI configuration files and scripts (example scopes: GitLabCI)", "c", None)
]
# fmt: on

