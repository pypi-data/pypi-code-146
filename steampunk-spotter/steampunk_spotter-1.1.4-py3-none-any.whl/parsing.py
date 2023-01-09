"""Provide methods for parsing Ansible artifacts."""

import sys
import uuid
from enum import Enum
from pathlib import Path
from typing import Dict, List, Tuple, Any, cast, Optional, Union

import pydantic.dataclasses
import yaml
from detect_secrets.core.secrets_collection import SecretsCollection
from detect_secrets.settings import default_settings
from yaml import MappingNode

# TODO: Rethink if we need to allow parsing and scanning files with other suffixes
YAML_SUFFIXES = (".yml", ".yaml")


@pydantic.dataclasses.dataclass
class ParsingResult:
    """A container for information about the parsed Ansible artifacts."""

    tasks: List[Dict[str, Any]]
    playbooks: List[Dict[str, Any]]

    def tasks_without_metadata(self) -> List[Dict[str, Any]]:
        """
        Remove sensitive data from input tasks.

        :return: Cleaned list of input tasks
        """
        return [
            {
                "task_id": t["task_id"],
                "task_args": t["task_args"]
            } for t in self.tasks
        ]

    def playbooks_without_metadata(self) -> List[Dict[str, Union[str, List[Dict[str, Any]]]]]:
        """
        Remove sensitive data from input playbooks.

        :return: Cleaned list of input playbooks
        """
        return [
            {
                "playbook_id": t["playbook_id"],
                "plays": [
                    {
                        "play_id": x.get("play_id", None),
                        "play_args": x["play_args"]
                    }
                    for x in t["plays"]
                ]
            } for t in self.playbooks
        ]


class SafeLineLoader(yaml.loader.SafeLoader):
    """YAML loader that adds line numbers."""

    def construct_mapping(self, node: MappingNode, deep: bool = False) -> Dict[Any, Any]:
        """
        Overridden the original construct_mapping method.

        :param node: YAML node object
        :param deep: Build objects recursively
        :return: A dict with loaded YAML
        """
        mapping: Dict[Any, Any] = \
            cast(Dict[Any, Any], super().construct_mapping(node, deep=deep))

        meta = {}
        meta["__line__"] = node.start_mark.line + 1
        meta["__column__"] = node.start_mark.column + 1
        meta["__start_mark_index__"] = node.start_mark.index
        meta["__end_mark_index__"] = node.end_mark.index
        mapping["__meta__"] = meta

        return mapping


class AnsibleArtifact(Enum):
    """Enum that can distinct between different Ansible artifacts (i.e., types of Ansible files)."""

    TASK = 1
    PLAYBOOK = 2
    ROLE = 3
    COLLECTION = 4


class _PlaybookKeywords:
    """
    Enum that stores significant keywords for playbooks that help us automatically discover Ansible file types.

    Keywords were gathered from: https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html.
    """

    PLAY = {
        "any_errors_fatal", "become", "become_exe", "become_flags", "become_method", "become_user", "check_mode",
        "collections", "connection", "debugger", "diff", "environment", "fact_path", "force_handlers", "gather_facts",
        "gather_subset", "gather_timeout", "handlers", "hosts", "ignore_errors", "ignore_unreachable",
        "max_fail_percentage", "module_defaults", "name", "no_log", "order", "port", "post_tasks", "pre_tasks",
        "remote_user", "roles", "run_once", "serial", "strategy", "tags", "tasks", "throttle", "timeout", "vars",
        "vars_files", "vars_prompt"
    }
    ROLE = {
        "any_errors_fatal", "become", "become_exe", "become_flags", "become_method", "become_user", "check_mode",
        "collections", "connection", "debugger", "delegate_facts", "delegate_to", "diff", "environment",
        "ignore_errors", "ignore_unreachable", "module_defaults", "name", "no_log", "port", "remote_user", "run_once",
        "tags", "throttle", "timeout", "vars", "when"
    }
    BLOCK = {
        "always", "any_errors_fatal", "become", "become_exe", "become_flags", "become_method", "become_user", "block",
        "check_mode", "collections", "connection", "debugger", "delegate_facts", "delegate_to", "diff", "environment",
        "ignore_errors", "ignore_unreachable", "module_defaults", "name", "no_log", "notify", "port", "remote_user",
        "rescue", "run_once", "tags", "throttle", "timeout", "vars", "when"
    }
    TASK = {
        "action", "any_errors_fatal", "args", "async", "become", "become_exe", "become_flags", "become_method",
        "become_user", "changed_when", "check_mode", "collections", "connection", "debugger", "delay", "delegate_facts",
        "delegate_to", "diff", "environment", "failed_when", "ignore_errors", "ignore_unreachable", "local_action",
        "loop", "loop_control", "module_defaults", "name", "no_log", "notify", "poll", "port", "register",
        "remote_user", "retries", "run_once", "tags", "throttle", "timeout", "until", "vars", "when"
    }


def _load_yaml_file(path: Path) -> Any:
    """
    Load YAML file and return corresponding Python object if parsing has been successful.

    :param path: Path to YAML file
    :return: Parsed YAML file as a Python object
    """
    with path.open() as stream:
        try:
            return yaml.load(stream, Loader=SafeLineLoader)
        except yaml.YAMLError as e:
            print(e, file=sys.stderr)
            return None
        except UnicodeDecodeError as e:
            print(f"{stream.name}: {e}", file=sys.stderr)
            return None


def _is_task_file(loaded_yaml: Any) -> bool:
    """
    Check if file is a task file = a YAML file containing one or more tasks in a list, where at least one task uses.

    keywords for tasks or blocks
    :param loaded_yaml: Parsed YAML file as a Python object
    :return: True or False
    """
    # use keywords for tasks and blocks
    task_file_keywords = (_PlaybookKeywords.TASK.union(_PlaybookKeywords.BLOCK))

    if isinstance(loaded_yaml, list):
        if any(len(task_file_keywords.intersection(e.keys())) > 0 for e in loaded_yaml if isinstance(e, dict)):
            return True

    return False


def _is_playbook(loaded_yaml: Any) -> bool:
    """
    Check if file is a playbook = a YAML file containing one or more plays in an list.

    :param loaded_yaml: Parsed YAML file as a Python object
    :return: True or False
    """
    # use only keywords that are unique for play and do not intersect with other keywords
    playbook_keywords = _PlaybookKeywords.PLAY.difference(
        _PlaybookKeywords.TASK.union(_PlaybookKeywords.BLOCK).union(_PlaybookKeywords.ROLE))

    if isinstance(loaded_yaml, list):
        if any(len(playbook_keywords.intersection(e.keys())) > 0 for e in loaded_yaml if isinstance(e, dict)):
            return True

    return False


def _is_role(directory: Path) -> bool:
    """
    Check if directory is a role = a directory with at least one of eight main standard directories.

    :param directory: Path to directory
    :return: True or False
    """
    standard_role_directories = ["tasks", "handlers", "library", "defaults", "vars", "files", "templates", "meta"]

    if any((directory / d).exists() for d in standard_role_directories):
        return True
    return False


def _is_collection(directory: Path) -> bool:
    """
    Check if directory is a collection = a directory with galaxy.yml or roles or plugins.

    :param directory: Path to directory
    :return: True or False
    """
    if (directory / "galaxy.yml").exists() or (directory / "roles").exists() or (directory / "plugins").exists():
        return True
    return False


def _clean_action_and_local_action(task: Dict[str, Any], parse_values: bool) -> None:
    """
    Handle parsing Ansible task that include action or local_action keys.

    This is needed because tasks from action or local_action have different syntax and need to be cleaned to look the
    same as other tasks.

    :param task: Ansible task
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Cleaned Ansible task
    """
    # TODO: Remove this spaghetti when API will be able to parse action plugins
    if parse_values:
        # server handles that case already
        return

    if not isinstance(task, dict):
        # probably inlined - we do not cover that case without parsed values
        return

    if not ("action" in task or "local_action" in task):
        # nothing to do
        return

    # replace action or local_action with the name of the module they contain and set delegate_to for local_action
    verb = "action" if "action" in task else "local_action"
    dict_with_module = next((d for d in list(task.values()) if isinstance(d, dict) and "module" in d), None)
    if dict_with_module is not None:
        module_name = dict_with_module.pop("module", None)
        action = task.pop(verb, None)
        task[module_name] = action
        if verb == "local_action":
            task["delegate_to"] = None


def _remove_deep_metadata(task: Any) -> Any:
    """
    Remove nested metadata.

    :param task: Ansible task
    :return: Updated Ansible task
    """
    if not task:
        return task

    if isinstance(task, dict):
        return {k: _remove_deep_metadata(v) for k, v in task.items() if k != "__meta__"}

    if isinstance(task, list):
        return [_remove_deep_metadata(x) for x in task]

    return task


def _remove_parameter_values(task: Dict[str, Any], params_to_keep: Optional[List[str]] = None) -> None:
    """
    Remove parameter values from Ansible tasks.

    :param task: Ansible task
    :param params_to_keep: List of parameters that should not be removed
    """
    for task_key in task:
        if isinstance(task[task_key], dict):
            for key in list(task[task_key]):
                if key != "__meta__":
                    task[task_key][key] = None
        else:
            if not params_to_keep or task_key not in params_to_keep:
                task[task_key] = None


def detect_secrets_in_file(file_name: str) -> List[str]:
    """
    Detect secret parameter values (e.g., passwords, SSH keys, API tokens, cloud credentials, etc.) in the file.

    :param file_name: Name of the original file with tasks
    """
    secret_values = []
    secrets_collection = SecretsCollection()
    with default_settings():
        secrets_collection.scan_file(file_name)
        for secret_set in secrets_collection.data.values():
            for secret in secret_set:
                if secret.secret_value:
                    secret_values.append(secret.secret_value)

    return secret_values


def _remove_secret_parameter_values(yaml_key: Any, secret_values: List[str]) -> Any:
    """
    Remove secret parameter values from YAML.

    :param yaml_key: YAML key
    :param secret_values: List of detected secret values
    :return: Updated YAML key
    """
    if isinstance(yaml_key, dict):
        return {k: _remove_secret_parameter_values(v, secret_values) for k, v in yaml_key.items()}

    if isinstance(yaml_key, list):
        return [_remove_secret_parameter_values(x, secret_values) for x in yaml_key]

    if isinstance(yaml_key, str) and any(secret_value in yaml_key for secret_value in secret_values):
        return None

    return yaml_key


def _parse_tasks(tasks: List[Dict[str, Any]], file_name: str, parse_values: bool = False) -> List[Dict[str, Any]]:
    """
    Parse Ansible tasks and prepare them for scanning.

    :param tasks: List of Ansible task dicts
    :param file_name: Name of the original file with tasks
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: List of parsed Ansible tasks
    """
    try:
        parsed_tasks = []
        for task in tasks:
            _clean_action_and_local_action(task, parse_values)
            if "block" in task:
                parsed_tasks += _parse_tasks(task["block"], file_name, parse_values)
                continue

            task_meta = task.pop("__meta__", None)

            if not parse_values:
                _remove_parameter_values(task)
            else:
                for task_key in task:
                    task[task_key] = _remove_secret_parameter_values(task[task_key], detect_secrets_in_file(file_name))

            meta = {
                "file": file_name,
                "line": task_meta["__line__"],
                "column": task_meta["__column__"],
                "start_mark_index": task_meta["__start_mark_index__"],
                "end_mark_index": task_meta["__end_mark_index__"]
            }

            task_dict = {
                "task_id": str(uuid.uuid4()),
                "task_args": _remove_deep_metadata(task),
                "spotter_metadata": meta
            }
            parsed_tasks.append(task_dict)

        return parsed_tasks
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error while parsing tasks from {file_name}: {e}", file=sys.stderr)
        return []


def _parse_play(play: Dict[str, Any], file_name: str, parse_values: bool = False) -> Dict[str, Any]:
    """
    Parse Ansible play and prepare it for scanning.

    :param play: Ansible play dict
    :param file_name: Name of the original file with play
    :param parse_values: True if also read values (apart from parameter names) from play parameters, False if not
    :return: Dict with parsed Ansible play
    """
    try:
        play_meta = play.pop("__meta__", None)

        if not parse_values:
            _remove_parameter_values(play, ["collections"])
        else:
            for play_key in play:
                play[play_key] = _remove_secret_parameter_values(play[play_key], detect_secrets_in_file(file_name))

        meta = {
            "file": file_name,
            "line": play_meta["__line__"],
            "column": play_meta["__column__"],
            "start_mark_index": play_meta["__start_mark_index__"],
            "end_mark_index": play_meta["__end_mark_index__"]
        }

        play_dict = {
            "play_id": str(uuid.uuid4()),
            "play_args": _remove_deep_metadata(play),
            "spotter_metadata": meta
        }

        return play_dict
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error while parsing play from {file_name}: {e}", file=sys.stderr)
        return {}


def _parse_playbook(playbook: List[Dict[str, Any]], file_name: str, parse_values: bool = False) -> \
        Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Parse Ansible playbook and prepare it for scanning.

    :param playbook: Ansible playbook as dict
    :param file_name: Name of the original file with playbook
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Tuple containing list of parsed Ansible tasks and parsed playbook as dict
    """
    parsed_tasks = []
    parsed_plays = []
    for play in playbook:
        tasks = play.pop("tasks", [])
        handlers = play.pop("handlers", [])

        if not isinstance(tasks, list):
            tasks = []
        if not isinstance(handlers, list):
            handlers = []

        parsed_tasks += _parse_tasks(tasks + handlers, file_name, parse_values)
        parsed_plays.append(_parse_play(play, file_name, parse_values))

    parsed_playbook = {"playbook_id": str(uuid.uuid4()), "plays": parsed_plays}
    return parsed_tasks, [parsed_playbook]


def _parse_role(directory: Path, parse_values: bool = False) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Parse Ansible role.

    :param directory: Role directory
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Tuple containing list of parsed Ansible tasks and parsed playbook as dict
    """
    parsed_role_tasks = []
    for task_file in (list((directory / "tasks").rglob("*")) + list((directory / "handlers").rglob("*"))):
        if task_file.is_file() and task_file.suffix in YAML_SUFFIXES:
            loaded_yaml = _load_yaml_file(task_file)
            if _is_task_file(loaded_yaml):
                parsed_role_tasks = _parse_tasks(loaded_yaml, str(task_file), parse_values)
    return parsed_role_tasks, []


def _parse_collection(directory: Path, parse_values: bool = False) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Parse Ansible collection.

    :param directory: Collection directory
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Tuple containing list of parsed Ansible tasks and parsed playbook as dict
    """
    parsed_collection_tasks = []
    parsed_collection_playbooks = []
    for role in (list((directory / "roles").rglob("*"))):
        if role.is_dir():
            parsed_tasks, _ = _parse_role(role, parse_values)
            parsed_collection_tasks += parsed_tasks
    for playbook in (list((directory / "playbooks").rglob("*"))):
        if playbook.is_file() and playbook.suffix in YAML_SUFFIXES:
            loaded_yaml = _load_yaml_file(playbook)
            if _is_playbook(playbook):
                parsed_tasks, parsed_playbooks = _parse_playbook(loaded_yaml, str(playbook), parse_values)
                parsed_collection_tasks += parsed_tasks
                parsed_collection_playbooks += parsed_playbooks
    for path in (list(directory.glob("*.yml")) + list(directory.glob("*.yaml"))):
        if path.is_file() and path.suffix in YAML_SUFFIXES:
            loaded_yaml = _load_yaml_file(path)
            if _is_playbook(path):
                parsed_tasks, parsed_playbooks = _parse_playbook(loaded_yaml, str(path), parse_values)
                parsed_collection_tasks += parsed_tasks
                parsed_collection_playbooks += parsed_playbooks
            elif _is_task_file(path):
                parsed_collection_tasks += _parse_tasks(loaded_yaml, str(path), parse_values)
    return parsed_collection_tasks, parsed_collection_playbooks


def parse_unknown_ansible_artifact(path: Path, parse_values: bool = False) -> \
        Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Parse Ansible artifact (unknown by type) by applying automatic Ansible file type detection.

    We are able to can discover task files, playbooks, roles and collections at any level recursively.

    :param path: Path to file or directory
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Tuple containing list of parsed Ansible tasks and parsed playbook as dict
    """
    parsed_ansible_artifacts_tasks = []
    parsed_ansible_artifacts_playbooks = []

    if path.is_file() and path.suffix in YAML_SUFFIXES:
        loaded_yaml = _load_yaml_file(path)
        if _is_playbook(loaded_yaml):
            parsed_tasks, parsed_playbooks = _parse_playbook(loaded_yaml, str(path), parse_values)
            parsed_ansible_artifacts_tasks += parsed_tasks
            parsed_ansible_artifacts_playbooks += parsed_playbooks
        elif _is_task_file(loaded_yaml):
            parsed_ansible_artifacts_tasks += _parse_tasks(loaded_yaml, str(path), parse_values)
    if path.is_dir():
        if _is_collection(path):
            parsed_tasks, parsed_playbooks = _parse_collection(path, parse_values)
            parsed_ansible_artifacts_tasks += parsed_tasks
            parsed_ansible_artifacts_playbooks += parsed_playbooks
        elif _is_role(path):
            parsed_tasks, parsed_playbooks = _parse_role(path, parse_values)
            parsed_ansible_artifacts_tasks += parsed_tasks
            parsed_ansible_artifacts_playbooks += parsed_playbooks
        else:
            for sub_path in path.rglob("*"):
                parsed_tasks, parsed_playbooks = parse_unknown_ansible_artifact(sub_path, parse_values)
                parsed_ansible_artifacts_tasks += parsed_tasks
                parsed_ansible_artifacts_playbooks += parsed_playbooks

    return parsed_ansible_artifacts_tasks, parsed_ansible_artifacts_playbooks


def parse_ansible_artifacts(paths: List[Path], parse_values: bool = False) -> ParsingResult:
    """
    Parse multiple Ansible artifacts.

    :param paths: List of paths to Ansible artifacts
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: ParsingResult object with list of parsed Ansible tasks and playbooks that are prepared for scanning
    """
    parsed_ansible_artifacts_tasks = []
    parsed_ansible_artifacts_playbooks = []
    for path in paths:
        if not path.exists():
            print(f"Error: Ansible artifact file at {path} provided for scanning does not exist.")
            sys.exit(1)

        parsed_tasks, parsed_playbooks = parse_unknown_ansible_artifact(path, parse_values)
        parsed_ansible_artifacts_tasks += parsed_tasks
        parsed_ansible_artifacts_playbooks += parsed_playbooks

    return ParsingResult(parsed_ansible_artifacts_tasks, parsed_ansible_artifacts_playbooks)
