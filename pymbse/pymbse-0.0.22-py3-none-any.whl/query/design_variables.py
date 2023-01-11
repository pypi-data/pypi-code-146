from pymbse.commons import json_file


def get_design_variable_from_local_variable_file_cache(design_variables_mode,
                                                       design_variables,
                                                       url="http://cache_rest:8000",
                                                       get_max_optimization_ix=None,
                                                       get_best_optimization_snapshot=None):
    if design_variables_mode == "LOCAL_FILE":
        return json_file.read("../input/design_variables.json")
    elif design_variables_mode == "BEST_SNAPSHOT":
        max_opt_ix = get_max_optimization_ix(url)
        return get_best_optimization_snapshot(url, max_opt_ix)["input_parameters"]["design_variables"]
    elif design_variables_mode == "VARIABLE":
        return design_variables
    else:
        raise AttributeError(f"Design variables mode {design_variables_mode} not supported")
