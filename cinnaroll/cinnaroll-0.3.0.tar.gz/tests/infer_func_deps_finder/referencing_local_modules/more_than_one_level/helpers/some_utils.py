import tests.infer_func_deps_finder.referencing_local_modules.more_than_one_level.helpers_helpers.some_utils_helpers_need as utils


def func_from_helpers() -> None:
    print("fizz")
    utils.func_from_helpers_helpers()
