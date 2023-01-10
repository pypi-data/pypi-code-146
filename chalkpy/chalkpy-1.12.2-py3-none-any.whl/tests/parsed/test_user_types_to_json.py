import json
import os
import pathlib

import tests
from chalk.importer import import_all_python_files_from_dir
from chalk.parsed.user_types_to_json import get_registered_types_as_json


def test_get_registered_types_as_json():
    """Functional test to ensure that we can import all registered types in the tests folder and convert them to JSON.
    Does not otherwise validate correctness."""
    tests_folder = pathlib.Path(os.path.abspath(os.path.dirname(tests.__file__)))
    import_all_python_files_from_dir(tests_folder)
    registered_types_json = get_registered_types_as_json(scope_to=tests_folder, failed=[])
    json.loads(registered_types_json)
