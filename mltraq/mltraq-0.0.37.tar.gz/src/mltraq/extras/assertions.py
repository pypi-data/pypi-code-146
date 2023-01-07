import pandas as pd
from mltraq.run import Run


class RunAssertion(Exception):
    """Raise this exception if an assertion on the runs state fails."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def assert_keys(name, keys, missing=False):
    if isinstance(keys, str):
        keys = [keys]

    def func(run: Run):
        for key in keys:
            if not missing and (key not in getattr(run, name)):
                raise RunAssertion(f"run.{name}['{key}'] missing.")
            if missing and (key in run[name]):
                raise RunAssertion(f"run.{name}['{key}'] already present.")

    return func


def assert_types(name, key_types):
    def func(run: Run):
        for key, key_type in key_types:
            assert_keys(name, key)
            if not isinstance(getattr(run, name)[key], key_type):
                raise RunAssertion(f"type(run.{name}) != {key_type}")

    return func


def assert_df(name, key, columns=None, n_rows=None):
    def func(run: Run):
        assert_types(name, {key: pd.DataFrame})
        if columns is not None:
            cols_df = list(getattr(run, name)[key].columns)
            cols_expected = list(columns)
            if set(cols_df) != set(cols_expected):
                raise RunAssertion(f"run.{name}['{key}'].columns == {cols_df} != {cols_expected}")
        if n_rows is not None:
            n_rows_df = len(getattr(run, name)[key])
            if n_rows_df != n_rows:
                raise RunAssertion(f"len(run.{name}['{key}']) == {n_rows_df} != {n_rows}")

    return func
