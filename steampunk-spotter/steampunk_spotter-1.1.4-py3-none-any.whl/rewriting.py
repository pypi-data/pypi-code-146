"""Provide rewriting - automated applying of suggestions to the code."""

import itertools
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

import pydantic.dataclasses
import yaml

OKGREEN = "\033[92m"
OKRED = "\033[0;31m"
ENDC = "\033[0m"


@pydantic.dataclasses.dataclass
class Suggestion:
    """Suggestion for rewriting Ansible task."""

    task_args: Dict[str, Any]
    file: Path
    file_parent: Path
    start_mark: int
    end_mark: int
    suggestion: Dict[str, Any]

    @classmethod
    def from_task(cls, task: Any, suggestion: Dict[str, Any]) -> "Suggestion":
        """
        Create Suggestion object for rewriting Ansible task.

        :param task: Ansible task content.
        :param suggestion: Suggestion as dict with action to do and data to use for update
        """
        task_args = task["task_args"]
        file_path = Path(task["spotter_metadata"]["file"])

        return cls(
            task_args=task_args,
            file=file_path,
            file_parent=file_path.parent,
            start_mark=task["spotter_metadata"]["start_mark_index"],
            end_mark=task["spotter_metadata"]["end_mark_index"],
            suggestion=suggestion
        )


def _update_content(content: str, suggestion: Suggestion, colorize: bool) -> Optional[Tuple[str, int]]:
    """
    Update task content.

    :param content: Old task content
    :param suggestion: Suggestion object for a specific task
    :param colorize: If True color things that will be changed
    :return: Tuple with updated content and content length difference, or none if matching failed.
    """
    suggestion_dict = suggestion.suggestion
    if suggestion_dict.get("action") != "FIX_FQCN":
        return content, 0

    part = content[suggestion.start_mark:suggestion.end_mark]
    before = suggestion_dict["data"]["before"]
    after = suggestion_dict["data"]["after"]
    regex = rf"([\t ]*)({before})(\s*:\s*)"

    replacement = f"{OKGREEN}{after}{ENDC}" if colorize else after
    match = re.search(regex, part, re.MULTILINE)
    if match is None:
        print("Applying suggestion failed: could not find string to replace.")
        return None

    s_index, e_index = match.span(2)
    end_content = content[:suggestion.start_mark + s_index] + replacement + content[suggestion.start_mark + e_index:]
    return end_content, len(replacement) - len(before)


def update_files(suggestions: List[Suggestion]) -> None:  # pylint: disable=too-many-locals
    """
    Update files by following suggestions.

    :param suggestions: List of suggestions as Suggestion objects
    """
    get_file_func = lambda x: x.file  # pylint: disable=unnecessary-lambda-assignment
    files = [(file, list(suggests)) for file, suggests in itertools.groupby(suggestions, get_file_func)]

    get_inode_func = lambda x: os.stat(x[0]).st_ino  # pylint: disable=unnecessary-lambda-assignment
    inodes = [next(group) for _, group in itertools.groupby(sorted(files, key=get_inode_func), get_inode_func)]

    requirements_update_suggestions = set()
    for file, suggests in inodes:
        suggestions_reversed = list(reversed(suggests))
        with file.open("r", encoding="utf-8") as f:
            content = f.read()

        end_content = content
        try:
            for suggestion in suggestions_reversed:
                suggestion_dict = suggestion.suggestion
                if suggestion_dict.get("action") == "FIX_REQUIREMENTS":
                    collection_name = suggestion_dict["data"]["collection_name"]
                    collection_version = suggestion_dict["data"]["version"]
                    # TODO: Update path when we are able to get it from scan input or scan result
                    requirements_yml_path = suggestion.file_parent / "requirements.yml"
                    requirements_update_suggestions.add((requirements_yml_path, collection_name, collection_version))
                    continue

                update_result = _update_content(end_content, suggestion, False)
                if update_result is None:
                    continue
                end_content, _ = update_result
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error when rewriting {f}: {e}")

        if end_content != content:
            with file.open("w", encoding="utf-8") as f:
                f.write(end_content)

    # TODO: Consider updating this when we will be updating detection and rewriting of collection requirements
    for requirements_yml_path, collection_name, collection_version in requirements_update_suggestions:
        with requirements_yml_path.open("a+", encoding="utf-8") as requirements_file:
            requirements_file.seek(0)
            try:
                data = yaml.safe_load(requirements_file)
            except yaml.YAMLError:
                # overwrite erroneous requirement file
                data = None
            if not data:
                data = {}
            if not isinstance(data, dict):
                # should we overwrite in this case as well?
                continue
            if "collections" not in data or ("collections" in data and data["collections"] is None):
                data["collections"] = []

            data["collections"].append({"name": collection_name, "version": collection_version})
            requirements_file.seek(0)
            requirements_file.truncate()
            requirements_file.write(yaml.dump(data, default_flow_style=False))
