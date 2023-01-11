import os
import subprocess
import sys
import traceback
from typing import Mapping, Sequence

import pkg_resources

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
    )
)

# Install required packages.
_REQUIRED_PKGS = {
    "numpy", "pandas", "scikit-learn"
}  # TODO(davidkurokawa): Stop using sklearn.
# for some reason pylint thinks pkg_resources.working_set is not iterable.
# pylint: disable=E1133
installed_pkgs = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
missing = _REQUIRED_PKGS - installed_pkgs.keys()
if missing:
    print(
        "The following packages are required, is it safe to install them: {}".
        format(missing)
    )
    print("Install them (y/n)?")
    while True:
        response = input().lower()
        if response in ["yes", "y"]:
            break
        elif response in ["no", "n"]:
            sys.exit(
                "Not given permission to install needed packages: {}".
                format(missing)
            )
        else:
            print(
                "Your response ('{}') was not one of the expected responses: y, n"
                .format(response)
            )
            print("Install them (y/n)?")
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing])

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from truera.public.feature_map import init_default_feature_map
from truera.public.feature_map import verify_feature_map
from truera.public.pyfunc_model import load_model

_DEFAULT_ARGS = {
    "package_directory": None,
    "pre": None,
    "post": None,
    "extra": None,
    "label": None,
    "default_map": None,
    "ot": None,
    "skip_confirmation": None,
    "id_column": None
}


def validate() -> None:
    args = read_args(_DEFAULT_ARGS)
    skip_confirmation = args["skip_confirmation"] == "True"
    pre_data, post_data, ys = validate_and_load_data(
        args["pre"],
        args["post"],
        args["extra"],
        args["label"],
        id_column=args["id_column"]
    )
    pre_columns = list(pre_data.columns)
    post_columns = list(post_data.columns)
    if args["default_map"] == "True" and args["pre"] and args[
        "post"] and args["pre"] != args["post"]:
        validate_feature_map(
            pre_columns, post_columns, post_data, skip_confirmation
        )
    model = validate_and_load_model(args["package_directory"])
    validate_accuracy(model, post_data, ys, args["ot"], skip_confirmation)


def validate_and_load_data(
    pre_filename,
    post_filename,
    extra_filename,
    label_filename,
    *,
    id_column=None
):
    try:
        assert_or_fail_with_message(
            pre_filename or post_filename,
            "At least one of the pre and post transformed data must be given!"
        )
        pre_filename = pre_filename or post_filename
        post_filename = post_filename or pre_filename
        pre_data = pd.read_csv(pre_filename)
        pre_data = pre_data.drop([id_column], axis=1) if id_column else pre_data
        post_data = pd.read_csv(post_filename)
        post_data = post_data.drop(
            [id_column], axis=1
        ) if id_column else post_data
        extra_data = pd.read_csv(extra_filename) if extra_filename else None
        if extra_data and id_column:
            extra_data = extra_data.drop([id_column], axis=1)
        header = None
        # This is done temporarily to support label file with and without header
        # for backward compatibility.
        if id_column:
            ys_df = pd.read_csv(label_filename, header=0)
            ys_df = ys_df.drop([id_column], axis=1)
        else:
            if "__internal_with_headers" in os.path.basename(label_filename):
                header = 0
            ys_df = pd.read_csv(label_filename, header=header)

        ys = ys_df.to_numpy()
        assert_or_fail_with_message(
            ys.ndim == 1 or (ys.ndim == 2 and ys.shape[1] == 1),
            "Provided labels must be 1D!"
        )
        ys = ys.ravel()
        list(pre_data.columns)
        list(post_data.columns)
    except:
        fail_with_stack_trace("Failed to read dataset!", traceback.format_exc())
    num_pre_transform_rows = pre_data.shape[0]
    assert_or_fail_with_message(
        num_pre_transform_rows == post_data.shape[0],
        "Pre and post transformed data must have the same number of rows!"
    )
    assert_or_fail_with_message(
        extra_data is None or num_pre_transform_rows == extra_data.shape[0],
        "Extra data must have the same number of rows as pre and post transformed data!"
    )
    assert_or_fail_with_message(
        ys is None or num_pre_transform_rows == ys.size,
        "Labels must have the same number of rows as pre and post transformed data!"
    )
    return pre_data, post_data, ys


def validate_feature_map(
    pre_columns, post_columns, post_data, skip_confirmation
):
    try:
        feature_map = init_default_feature_map(pre_columns, post_data)
        verify_feature_map(feature_map, pre_columns, post_columns)
        _print_feature_map(feature_map, post_columns, skip_confirmation)
    except:
        fail_with_stack_trace(
            "Failed to display feature map!", traceback.format_exc()
        )


def validate_and_load_model(package_directory):
    try:
        return load_model(package_directory)
    except:
        fail_with_stack_trace("Failed to load model!", traceback.format_exc())


def assert_or_fail_with_message(condition, message):
    if not condition:
        sys.exit(message)


def validate_accuracy(
    model, post_data, ys, model_output_type, skip_confirmation
):
    try:
        ys_pred = model.predict(post_data)
    except:
        fail_with_stack_trace(
            "Failed to run model on data!", traceback.format_exc()
        )
    try:
        _print_accuracy(
            ys, ys_pred, model_output_type != "regression", skip_confirmation
        )
    except:
        fail_with_stack_trace(
            "Failed to compute accuracy!", traceback.format_exc()
        )


def fail_with_stack_trace(base_message, stack_trace):
    message = "{} Here is the error:".format(base_message)
    divisor = "---------------------------------------------------"
    message = "{}\n{}\n{}{}".format(message, divisor, stack_trace, divisor)
    sys.exit(message)


def read_args(expected_args: Mapping[str, str]) -> Mapping[str, str]:
    # To read the args, we use a bare-bones sys.argv approach to avoid unnecessary dependencies.
    ret = expected_args.copy()
    for arg in sys.argv[1:]:
        assert arg[:2] == "--", "Arguments must start with --!"
        index_of_equal = arg.find("=")
        assert index_of_equal != -1, "No value for argument {} given!".format(
            arg
        )
        flag = arg[2:index_of_equal]
        value = arg[(index_of_equal + 1):]
        assert flag in ret, "Unexpected flag {} given!".format(flag)
        ret[flag] = value
    return ret


def _print_feature_map(
    feature_map: Mapping[str, str], all_post_features: Sequence[str],
    skip_confirmation: bool
) -> None:
    print("\nFEATURE MAP (CHECK THE FOLLOWING IS SENSIBLE):")
    for pre_feature, post_feature_idxs in feature_map.items():
        post_features = [all_post_features[i] for i in post_feature_idxs]
        print("{}: [{}]".format(pre_feature, ", ".join(post_features)))
    if not skip_confirmation:
        input("\nPress Enter to continue...\n")


def _print_accuracy(
    ys: np.ndarray, ys_pred: np.ndarray, is_classification: bool,
    skip_confirmation: bool
) -> None:
    if is_classification is None:
        is_classification = np.unique(ys) <= 2
    print(
        "Model is assumed to be a {} model".
        format("classification" if is_classification else "regression")
    )
    assert ys_pred.shape[0
                        ] == ys.size, "Model did not give right sized response!"
    if is_classification:
        assert ys_pred.shape[
            1] == 2, "Model did not give (num_rows, 2) shaped response!"
        auc = roc_auc_score(ys, ys_pred.iloc[:, 1])
        print("AUC = {}".format(auc))
    else:
        rmse = np.sqrt(np.mean((ys - ys_pred)**2))
        print("RMSE = {}".format(rmse))
    if not skip_confirmation:
        input("\nPress Enter to continue...\n")


if __name__ == "__main__":
    validate()
