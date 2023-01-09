from collections import namedtuple
from typing import List, Optional

from cinnaroll_internal import constants
from cinnaroll_internal.infer_func_deps_finder import output_verification
from cinnaroll_internal.infer_func_deps_finder.global_variables import VariableWithPositionInLine

# opening and loading can fail but if they do then the whole app's broken,
# so I don't see a point in handling this
LOAD_PICKLED_GLOBALS_STATEMENT = f"""
user_globals_file = open("{constants.GLOBAL_VARS_DICT_FILENAME}.pickle", "rb")
{constants.GLOBAL_VARS_DICT_NAME} = pickle.load(user_globals_file)
user_globals_file.close()
"""


InferFileContents = namedtuple("InferFileContents", ("test", "output"))


def infer_code_with_class_and_function_deps(
    infer_code: str, classes_and_functions_code: str
) -> str:
    return classes_and_functions_code + "\n\n" + infer_code


def build_infer_py_files_content(
    infer_code: str,
    import_statements: str,
    used_global_variables_locations: Optional[List[List[VariableWithPositionInLine]]],
) -> InferFileContents:
    if used_global_variables_locations:
        import_statements = "\n".join(
            [import_statements, "import pickle"]
        )

        code = replace_occurrences_of_global_vars_with_getting_them_from_globals_dict(
            infer_code, used_global_variables_locations
        )
    else:
        code = infer_code

    pickled_globals_loading = LOAD_PICKLED_GLOBALS_STATEMENT if used_global_variables_locations else ""
    infer_test = f"\n\ninfer({output_verification.INFER_MODEL_OBJECT_ARG_NAME}," \
                 f" {output_verification.INFER_INPUT_DATA_ARG_NAME})"

    test_file_content = (
        import_statements + "\n\n" + code + "\n\n" + infer_test
    )
    output_file_content = (
        import_statements + "\n\n" + pickled_globals_loading + "\n\n" + code
    )

    return InferFileContents(test_file_content, output_file_content)


def replace_occurrences_of_global_vars_with_getting_them_from_globals_dict(
    code: str, variables_to_replace: List[List[VariableWithPositionInLine]]
) -> str:
    code_lines = code.splitlines()
    code_using_globals_dict = replace_vars_with_globals_dict_usage(
        code_lines, variables_to_replace
    )

    return "\n".join(code_using_globals_dict)


def replace_vars_with_globals_dict_usage(
    code_lines: List[str], variables_to_replace: List[List[VariableWithPositionInLine]]
) -> List[str]:
    added_chars_count = len(f"{constants.GLOBAL_VARS_DICT_NAME}['']")
    lines_count = len(variables_to_replace)
    for line_number in range(lines_count):
        vars_count = len(variables_to_replace[line_number])
        for i in range(vars_count):
            var = variables_to_replace[line_number][i]
            offset = added_chars_count

            code_lines[line_number] = (
                code_lines[line_number][: var.start_column]
                + f"{constants.GLOBAL_VARS_DICT_NAME}['{var.name}']"
                + code_lines[line_number][var.start_column + var.name_length:]
            )
            for j in range(i, vars_count):
                variables_to_replace[line_number][j].start_column += offset

    return code_lines
