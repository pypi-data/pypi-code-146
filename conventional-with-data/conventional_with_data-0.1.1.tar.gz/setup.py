# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cz_conventional_with_data', 'questions']
install_requires = \
['commitizen>=2.39.1,<3.0.0']

setup_kwargs = {
    'name': 'conventional-with-data',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Conventional With Data\n\nA branch of conventionalish with an added `data` prefix.\n\nPatch Commitizen\'s Conventional Commits implementation with additional prefixes.\n\n```\nQUESTIONS = [\n    ("fix", "A bug fix", "x", PATCH),\n    ("feat", "A new feature", "f", MINOR),\n    ("data", "Changes to non-code input (data, blog content, models, etc.)", "a", PATCH),\n    ("docs", "Documentation only changes", "d", None),\n    ("style", "Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.)", "s", None),\n    ("refactor", "A code change that neither fixes a bug nor adds a feature", "r", PATCH),\n    ("perf", "A code change that improves performance", "p", PATCH),\n    ("test", "Adding missing or correcting existing tests", "t", None),\n    ("build", "Changes that affect the build system or external dependencies (example scopes: pip, docker, npm)", "b", None),\n    ("ci", "Changes to our CI configuration files and scripts (example scopes: GitLabCI)", "c", None)\n]\n```\n\nBy default, Commitizen will use its Conventional Commits implementation, so when you run `cz commit`, you will get a choice of \n\n* `fix:`\n* `feat:`\n* `docs:`\n* `style:`\n* `refactor:`\n* `perf:`\n* `test:`\n* `build:`\n* `ci:`\n\nCommitizen has a robust system for building your own commit patterns, and it\'s great if you want to start from scratch. But if you want to make a small change to the defaults and keep the nice prompts, commit-message linting, and changelog-building provided by Commitizen, you will have to create or update six patterns or regexps. This script inherits from ConventionalCommitsCz and patches in new choices and associated properties. FWIW, despite the *ish* in the name conventional*ish*, these changes will still meet the Conventional Commits standard (at least as much as Commitizen does) as long as the `feat:` and `fix:` prefixes remain.\n\nShould you want to accomplish this by hand:\n\n1. inherit from ConventionalCommitsCz\n2. overload `.questions()`  *# for commit prompts*\n3. overload `.schema_pattern()`  *# for commit-message linting*\n\n*Will your addition affect versioning?*\n\n4. overload `.bump_pattern`  *# for commitizen bump*\n5. overload `.bump_map`  *# for commitizen bump*\n6. overload `.commit_parser`  *# for commitizen changelog*\n7. overload `.change_type_map`  *# for commitizen changelog* \n8. overload `.changelog_pattern`  *# for commitizen changelog*\n\n## Usage\n\nTo make these changes using a script:\n\n1. clone this project into your project root\n2. edit the `QUESTIONS` value at the top of `questions.py`. The default value will give near-identical behavior to the Commitizen default.\n3. install conventionalish in your project venv (`poetry add .\\conventionalish`; `pip install .\\conventionalish`; ...) or upload to PyPi with a new name.\n4. run with `cz -n cz_conventionalish` or add the following to `pyproject.toml`\n\n~~~\n[tool.commitizen]\nname = "cz_conventionalish"\n~~~\n\n## Troubleshooting, Q&A\n\n**I updated the file, but Commitizen doesn\'t recognize the changes.**\n\nThis is an installed package, depending how you installed it, you may need to:\n\n1. delete any `commitizenish/build` or `commitizenish/egg-info` directories\n2. uninstall\n3. reinstall\n\n**How can I change the project name (`conventionalish`)?**\n\n1. change the name of this folder after you clone it\n2. update the line `name="conventionalish"` in `conventionalish/pyproject.toml` to `name="new_folder_name"`\n\n**How can I change the commit-rule name (`cz_conventionalish`)?**\n\n1. change the filename `conventionalish/cz_conventionalish.py` to `conventionalish/cz_new_name.py`\n2. change the line `{ include = "cz_conventionalish.py" }` in `conventionalish/pyproject.toml` to `{ include = "cz_new_name.py" }`\n\n## Author\nShay Hill (shay_public@hotmail.com)\n',
    'author': 'Shay Hill',
    'author_email': 'shay_public@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
