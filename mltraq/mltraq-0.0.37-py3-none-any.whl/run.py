import random
from functools import partial
from typing import Callable, List, Union

import numpy as np
import pandas as pd
from mltraq import options
from mltraq.job import Job
from mltraq.storage.database import next_ulid
from mltraq.utils.dicts import ObjectDictionary, product_dict
from mltraq.utils.frames import json_normalize, reorder_columns
from mltraq.utils.log import compact_exception_message
from mltraq.utils.text import stringify


class RunException(Exception):
    """Raised if there's a failure during the execution of functions on runs."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Runs(dict):
    """_summary_

    Args:
        dict (_type_): _description_
    """

    def __init__(self, runs=None):
        if runs is None:
            runs = []
        elif isinstance(runs, Runs):
            runs = runs.values()

        super().__init__({run.id_run: run for run in runs})

    # def map(self, f, *args, **kwargs):
    #    return [f(run, *args, **kwargs) for run in self.values()]

    def add(self, *runs):
        for run in runs:
            if isinstance(run, Run):
                self[run.id_run] = run
            elif isinstance(run, Runs):
                for k, v in run.items():
                    self[k] = v

    def first(self):
        return self[next(iter(self))]

    def next(self):
        run = Run()
        self[run.id_run] = run
        return run

    def df(self, max_level=0):
        # Load the dataframe from a dict or list of dicts.

        if len(self) == 0:
            # no runs!
            return pd.DataFrame(columns=["id_run"])

        df = json_normalize([{**run.fields, **{"id_run": run.id_run}} for run in self.values()], max_level=max_level)

        return reorder_columns(df, ["id_run"])

    def execute(
        self,
        steps: Union[Callable, List[Callable]] = None,
        kwargs=None,
        backend=None,
        n_jobs=-1,
    ):
        if not backend:
            backend = options.get("execution.default_backend")

        if len(self) == 0:
            # If no runs are defined and we execute the experiment, a dummy one is created.
            self.add(Run())

        tasks = [run.execute_func(steps=steps, kwargs=kwargs) for run in self.values()]

        random.Random(options.get("reproducibility.random_seed")).shuffle(tasks)

        # Randomize the order of the runs to execute.
        # ids_run = self.runs.get_ids()

        # if n_jobs == 1:
        #    with options.option_context(["tqdm.disable", True]):
        #        executed_runs = Job(tasks, n_jobs=n_jobs, backend=backend).execute()
        # else:
        executed_runs = Job(tasks, n_jobs=n_jobs, backend=backend).execute()

        # Check for exceptions, and raise first one encountered.
        for run in executed_runs:
            if run.exception is not None:
                raise run.exception

        # If no exceptions, update runs. Runs are updated only if all of them are successful.

        # Update runs, setting attribute values. The original objects are retained.

        # Point the runs to new instances that contain the result of the execution.
        for run in executed_runs:
            self[run.id_run] = run

        # for run in executed_runs:
        #    for attr in run.attrs:
        #        setattr(self[run.id_run], attr, getattr(run, attr))

    def _repr_html_(self):
        return f"Runs(keys({len(self)})={stringify(self.keys())})"


class Run:
    """A run represents an instance of the experiment, obtained by
    combining the fixed and variable parameters. The Run objects
    (and the tracked fields)  must be serializable with cloudpickle.
    """

    # 1. We ignore "steps" as functions are often problematic to handle correctly.
    attrs = [
        "id_run",
        "kwargs",
        "params",
        "fields",
        "locals",
        "exception",
    ]

    def __init__(
        self,
        id_run: str = None,
        steps: Union[Callable, List[Callable]] = None,
        kwargs: dict = None,
        params: dict = None,
        fields: dict = None,
    ):
        """Create a new run.

        Args:
            kwargs (dict, optional): Fixed parameters for all runs of an experiment. Defaults to None.
            parameters (dict, optional): Variable parameters to be considered for this run. Defaults to None.
            fields (dict, optional): fields to be tracked. Defaults to None.
            steps (Union[Callable, List[Callable]], optional): One or more functions to be executed. Their
            only parameter is an instance of the Run class itself.
            experiment_name (str, optional): Name of the experiment the run belongs to. Defaults to None.
        """

        self.id_run = next_ulid() if id_run is None else id_run
        self.kwargs = ObjectDictionary(kwargs)
        self.params = ObjectDictionary(params)
        self.fields = ObjectDictionary(fields)
        self.locals = ObjectDictionary(fields)

        # Execution state and steps to be executed
        self.steps = normalize_steps(steps)
        self.exception = None

        # attrs controls which fields are considered for pickling and unpickling, ignoring the others.

    def __getstate__(self):
        # Limit serialization to certain attributes, skipping those that are temporary and that might
        # cause serialization problems, such as self.steps .

        # From https://docs.python.org/3/library/pickle.html#pickle-protocol:
        # __init__() is not called when unpickling an instance
        # This means that we must set all fields in __getstate__(), otherwise they'll be missing upon unpickling.

        # Runs are unpickled when:
        # - Joblib.parallel returns executed runs
        # - Joblib.Memory returns cached runs
        # In both cases, we should not use the value of run.steps.

        state = {key: getattr(self, key) for key in Run.attrs}
        state["steps"] = []
        return state

    def __setitem__(self, key, item):
        self.fields[key] = item

    def __getitem__(self, key):
        return self.fields[key]

    def execute_func(self, steps=None, kwargs=None):
        return partial(lambda run: run.execute(steps=steps, kwargs=kwargs), self)

    def execute(self, steps=None, kwargs=None):
        # Determine random seed for this run, combining the UUID of the run and the
        # value of "reproducibility.random_seed".
        random_seed = (self.id_run.int + options.get("reproducibility.random_seed")) % (2**32 - 1)
        np.random.seed(random_seed)

        if steps is not None:
            self.steps = normalize_steps(steps)
        else:
            steps = []

        if kwargs is not None:
            self.kwargs = ObjectDictionary(kwargs)
        else:
            self.kwargs = ObjectDictionary({})

        self.exception = None

        for step in self.steps:
            try:
                step(self)
            except Exception as e:  # noqa
                self.exception = RunException(compact_exception_message(e))
                break

        return self

    def verify(self, func):
        func(self)

    def _repr_html_(self):
        return f'Run(id="{self.id_run}")'

    def df(self, max_level=0):
        # Load the dataframe from a dict or list of dicts.

        df = json_normalize([{**run.fields, **{"id_run": run.id_run}} for run in [self]], max_level=max_level)

        return reorder_columns(df, ["id_run"])


def normalize_steps(steps):
    if steps is None:
        return []
    elif callable(steps):
        return [steps]
    else:
        return steps


def get_params_list(**kwargs):
    if not kwargs:
        return [{}]
    params_list = list(product_dict(**kwargs))
    random.Random(options.get("reproducibility.random_seed")).shuffle(params_list)
    return params_list
