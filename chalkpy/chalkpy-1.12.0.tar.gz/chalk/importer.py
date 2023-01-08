import importlib
import importlib.util
import os
import sys
import traceback
from pathlib import Path
from typing import Callable, List

from pydantic import BaseModel

from chalk.gitignore.gitignore_parser import parse_gitignore
from chalk.utils.log_with_context import get_logger
from chalk.utils.paths import get_directory_root

_logger = get_logger(__name__)


def py_path_to_module(path: Path, repo_root: Path) -> str:
    try:
        p = path.relative_to(repo_root)
    except ValueError:
        p = path
    return str(p)[: -len(".py")].replace("./", "").replace("/", ".")


class FailedImport(BaseModel):
    filename: str
    module: str
    traceback: str


def import_all_python_files() -> List[FailedImport]:
    project_root = get_directory_root()
    if project_root is None:
        return [
            FailedImport(
                filename="",
                module="",
                traceback="Could not find chalk.yaml in this directory or any parent directory",
            )
        ]
    return import_all_python_files_from_dir(project_root=project_root)


def _search_recursively_for_file(base: Path, filename: str) -> List[Path]:
    ans = []
    assert base.is_dir()
    while True:
        filepath = base / filename
        if filepath.exists():
            ans.append(filepath)
        parent = base.parent
        if parent == base:
            return ans
        base = parent


def _is_relevant(x: Path, matching_functions: List[Callable[[Path], bool]]):
    return all((not match(x) for match in matching_functions))


def import_all_python_files_from_dir(project_root: Path) -> List[FailedImport]:
    project_root = project_root.absolute()
    matching_functions: List[Callable[[Path], bool]] = []
    matching_functions.extend(parse_gitignore(str(x)) for x in _search_recursively_for_file(project_root, ".gitignore"))
    matching_functions.extend(
        parse_gitignore(str(x)) for x in _search_recursively_for_file(project_root, ".chalkignore")
    )
    matching_functions.append(lambda x: x.name == "setup.py")

    cwd = os.getcwd()
    os.chdir(project_root)
    repo_root = Path(project_root)

    # If we don't import both of these, we get in trouble.
    sys.path.append(str(repo_root.resolve()))
    sys.path.append(str(repo_root.parent.resolve()))

    repo_files = sorted({p.resolve() for p in repo_root.glob("**/*.py") if p.is_file()})

    _logger.debug(f"REPO_ROOT: {repo_root.resolve()}")
    # _logger.debug(f"REPO_FILES: {repo_files}")

    venv = os.environ.get("VIRTUAL_ENV")
    module_paths = [
        (py_path_to_module(repo_file, repo_root), repo_file)
        for repo_file in repo_files
        if venv is None or Path(venv) not in repo_file.parents
    ]

    errors: List[FailedImport] = []
    for (module_path, filename) in module_paths:
        if (
            module_path.startswith(".eggs")
            or module_path.startswith("venv")
            or not _is_relevant(filename, matching_functions)
        ):
            continue

        try:
            importlib.import_module(module_path)
        except Exception:
            filename = filename.resolve()
            # relevant_file = any("from chalk." or "import chalk." in c for c in f)
            # if relevant_file:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            tb = traceback.extract_tb(ex_traceback)
            line = 0
            for i, l in enumerate(tb):
                if filename == Path(l.filename).resolve():
                    line = i
                    break

            relevant_traceback = f"""Exception in module {module_path}:
{os.linesep.join(traceback.format_tb(ex_traceback)[line:])}
\n{ex_type and ex_type.__name__}: {str(ex_value)}
"""
            errors.append(
                FailedImport(
                    traceback=relevant_traceback,
                    filename=str(filename),
                    module=module_path,
                )
            )

            _logger.debug(f"Failed while importing {module_path}", exc_info=True)
            continue

    os.chdir(cwd)
    return errors
