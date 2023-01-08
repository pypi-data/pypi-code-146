"""Edit conventional commits from commitizen.

Update the `questions` list to build your own Conventional-Commits style in
Committizen.

I drag this template file around to add prefixes like "content" to commit messages
for versioned websites or other creative content. To add a new prefix:

1. update ProjectCommitsCZ.questions
2. update ProjectCommitsCZ.schema_pattern

Will the addition affect versioning?

1. update bump_pattern
2. update bump_map
3. update commit_parser
4. update ProjectCommitsCZ.change_type_map
5. update changelog_pattern

:author: Shay Hill
:created: 2023-01-01
"""

from commitizen.defaults import Questions, MAJOR, MINOR, PATCH
from commitizen.cz.conventional_commits import ConventionalCommitsCz
from collections import OrderedDict

# fmt: off
# add or subtract questions here: (prefix, name, key, semver)
# semver is [MINOR, PATCH, or None], *not* MAJOR. MAJOR is always identified with
# "BREAKING CHANGE".
questions = [
    ("fix", "A bug fix", "x", PATCH),
    ("feat", "A new feature", "f", MINOR),
    ("data", "Changes to content (data, blog articles, designs, etc.)", "a", PATCH),
    ("docs", "Documentation only changes", "d", None),
    ("style", "Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.)", "s", None),
    ("refactor", "A code change that neither fixes a bug nor adds a feature", "r", PATCH),
    ("perf", "A code change that improves performance", "p", PATCH),
    ("test", "Adding missing or correcting existing tests", "t", None),
    ("build", "Changes that affect the build system or external dependencies (example scopes: pip, docker, npm)", "b", None),
    ("ci", "Changes to our CI configuration files and scripts (example scopes: GitLabCI)", "c", None)
]
# fmt: on


### STOP HERE - EVERYTHING ELSE IS AUTOMATED ###
### STOP HERE - EVERYTHING ELSE IS AUTOMATED ###
### STOP HERE - EVERYTHING ELSE IS AUTOMATED ###
### STOP HERE - EVERYTHING ELSE IS AUTOMATED ###
### STOP HERE - EVERYTHING ELSE IS AUTOMATED ###
### STOP HERE - EVERYTHING ELSE IS AUTOMATED ###
### STOP HERE - EVERYTHING ELSE IS AUTOMATED ###
### STOP HERE - EVERYTHING ELSE IS AUTOMATED ###


_patch_prefixes = [p for p, *_, v in questions if v == PATCH]
_minor_prefixes = [p for p, *_, v in questions if v == MINOR]


def _build_choices() -> list[dict[str, str]]:
    choices: list[dict[str, str]] = []
    for prefix, name, key, semver in questions:
        name = f"{prefix}: {name}"
        if semver is not None:
            name += f". Correlates with {semver} in SemVer"
        choices.append({"value": prefix, "name": name, "key": key})
    return choices


def _build_bump_pattern():
    types = "|".join(_minor_prefixes + _patch_prefixes)
    return rf"^(BREAKING[\-\ ]CHANGE|{types})(\(.+\))?(!)?"


def _build_bump_map():
    bump_map: OrderedDict[str, str]
    bump_map = OrderedDict(((r"^.+!$", MAJOR), (r"^BREAKING[\-\ ]CHANGE", MAJOR)))
    for prefix, *_ in (x for x in questions if x[3] == MINOR):
        bump_map[f"^{prefix}"] = MINOR
    for prefix, *_ in (x for x in questions if x[3] == PATCH):
        bump_map[f"^{prefix}"] = PATCH
    return bump_map


def _build_schema_pattern():
    """Commitizen added chore, revert, and bump. Keeping all three in the schema even
    though it would probably be best to just add them (at least the first two) as
    type_choices.
    """
    types = sorted([p for p, *_ in questions])
    for addition in ("chore", "revert", "bump"):
        if addition not in types:
            types.append(addition)
    prefixes = "|".join(types)
    return (
        r"(?s)"  # To explictly make . match new line
        rf"({prefixes})"  # type
        r"(\(\S+\))?!?:"  # scope
        r"( [^\n\r]+)"  # subject
        r"((\n\n.*)|(\s*))?$"
    )


def _build_commit_parser():
    semvers = "|".join(_minor_prefixes + _patch_prefixes + ["BREAKING CHANGE"])
    return (
        rf"^(?P<change_type>{semvers})"
        + r"(?:\((?P<scope>[^()\r\n]*)\)|\()?(?P<breaking>!)?:\s(?P<message>.*)?"
    )


def _build_change_type_map():
    semvers = reversed(_patch_prefixes + _minor_prefixes)
    return {p: p.title() for p in semvers}


class ConventionalishCz(ConventionalCommitsCz):
    bump_pattern = _build_bump_pattern()
    bump_map = _build_bump_map()
    commit_parser = _build_commit_parser()
    change_type_map = _build_change_type_map()
    changelog_pattern = _build_bump_pattern()

    def questions(self) -> Questions:
        questions = super().questions()
        questions[0]["choices"] = _build_choices()
        return questions

    def schema_pattern(self) -> str:
        return _build_schema_pattern()


discover_this = ConventionalishCz
