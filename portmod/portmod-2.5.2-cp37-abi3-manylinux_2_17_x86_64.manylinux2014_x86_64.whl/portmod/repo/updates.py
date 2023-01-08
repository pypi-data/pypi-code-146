# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""A module for parsing package updates"""

import os
from collections import defaultdict
from typing import Any, Dict, Optional

from portmod.globals import env
from portmod.repos import Repo
from portmodlib.parsers.list import read_list

_UPDATES: Optional[Dict[str, Dict[str, Any]]] = None


def get_moved(repo: Repo) -> Dict[str, str]:
    global _UPDATES
    if _UPDATES is None:
        _UPDATES = {}
        for repo in env.REPOS:
            parse_updates(repo)

    assert _UPDATES is not None
    return _UPDATES.get(repo.name, {}).get("move", {})


def parse_updates(repo: Repo):
    global _UPDATES
    path = os.path.join(repo.location, "profiles", "updates")
    repo_updates: Dict[str, Any] = defaultdict(dict)

    def parse_file(filename: str):
        result: Dict[str, Dict[str, Any]] = defaultdict(dict)
        for line in read_list(filename):
            command, _, arguments = line.partition(" ")
            if command == "move":
                source, target = arguments.split(" ")
                source = source.strip()
                target = target.strip()
                result["move"][source] = target
        return result

    if os.path.exists(path):
        for filename in os.listdir(path):
            for key, value in parse_file(os.path.join(path, filename)).items():
                repo_updates[key].update(value)

    assert _UPDATES is not None
    _UPDATES[repo.name] = repo_updates
