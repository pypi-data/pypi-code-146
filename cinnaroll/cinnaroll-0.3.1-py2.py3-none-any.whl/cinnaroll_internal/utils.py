import inspect
import os
from dataclasses import dataclass
from pathlib import Path, PosixPath
import re
import shutil
from typing import List, Any, Union, Optional, Callable, Dict

from cinnaroll_internal.constants import BACKEND_BASE_URL


@dataclass
class MockResponse:
    status_code: int
    json_data: Dict[str, str]

    def json(self) -> Dict[str, str]:
        return self.json_data

    def __str__(self) -> str:
        return f"status: {self.status_code}, response: {self.json_data}"


def mock_request(*args: Any, **kwargs: Any) -> MockResponse:
    print("\n<mock_request>")
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")

    if args[0].startswith(f"{BACKEND_BASE_URL}/modelUpload?projectId"):
        res = MockResponse(200, {})
    elif args[0] == f"{BACKEND_BASE_URL}/modelUploads":
        res = MockResponse(
            201,
            {
                "id": "abc123",
                "status": "great",
                "uploadUrl": f"{BACKEND_BASE_URL}/unique_upload_url",
            },
        )
    elif args[0] == f"{BACKEND_BASE_URL}/unique_upload_url":
        res = MockResponse(200, {"status": "good"})
    elif args[0] == f"{BACKEND_BASE_URL}/modelUploads/abc123":
        res = MockResponse(200, {"status": "good"})
    else:
        res = MockResponse(404, {"page not found": "get lost"})

    print(f"\n{res}")
    print("</mock_request>\n")
    return res


def append_if_not_none(iterable: List[Any], item: Optional[Any]) -> None:
    if item is not None:
        iterable.append(item)


# todo: unittest
def get_uncommented_lines(code: str) -> List[str]:
    uncommented_code = re.sub(
        re.compile('( *#.*)|"""[\\d\\D]*?"""'), "", code
    )
    lines = uncommented_code.splitlines()

    output_lines: List[str] = []

    for line in lines:
        if len(line.lstrip()):
            output_lines.append(line)

    output_lines.append("")

    return output_lines


def get_function_code_without_comments(function: Callable) -> str:  # type: ignore
    code = inspect.getsource(function)
    name = function.__name__
    return remove_surplus_indent_and_comments_from_function_code(code, name)


def remove_surplus_indent_and_comments_from_function_code(function_code: str, function_name: str) -> str:
    lines = get_uncommented_lines(function_code)
    chars_to_trim = len(lines[0]) - len(lines[0].lstrip())
    lines = [line[chars_to_trim:] for line in lines]
    # delete @staticmethod etc.
    while f"def {function_name}(" not in lines[0]:
        lines = lines[1:]
    return "\n".join(lines)


def is_function_implemented(function: Callable) -> bool:  # type: ignore
    code = get_function_code_without_comments(function)
    lines = get_uncommented_lines(code)

    lines[0] = re.sub(re.compile("#.*"), "", lines[0]).rstrip(" ")
    if lines[0][-3:] == "...":
        return False
    if lines[1].lstrip() in ("pass", "..."):
        return False
    return True


def clean_path(path: Union[Path, PosixPath], leave_empty_folder: bool = False) -> None:
    """If path is a file, remove it. If path is a folder remove it or empty it depending on the second parameter."""
    if path.exists():
        if path.is_file():
            os.remove(path)
        elif path.is_dir():
            shutil.rmtree(path)

            if leave_empty_folder:
                path.mkdir()
        else:
            raise RuntimeWarning(f"Unknown object: {path}")
