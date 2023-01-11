import os
from contextlib import contextmanager
from pathlib import Path
from pprint import pformat

from snek5000.util.gfortran_log import log_matches

import pytest

import numpy as np


def pytest_addoption(parser):
    # https://pytest.readthedocs.io/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


@contextmanager
def unset_snek_debug():
    old_snek_debug = os.environ.pop("SNEK_DEBUG", None)
    try:
        yield
    finally:
        if old_snek_debug is not None:
            os.environ["SNEK_DEBUG"] = old_snek_debug


@pytest.fixture(scope="module")
def sim_cbox_executed():
    from snek5000_cbox.solver import Simul

    params = Simul.create_default_params()
    params.output.sub_directory = "tests_snek5000"

    params.nek.general.stop_at = "numSteps"
    params.nek.general.dt = 1e-3
    params.nek.general.num_steps = 12
    params.nek.general.write_interval = 3

    params.Ra_side = 100
    params.oper.nproc_min = 2
    params.oper.nproc_max = 12
    params.oper.dim = 2
    params.oper.nx = params.oper.ny = 8

    coords = [(0.5, 0.5)]
    params.output.history_points.write_interval = 2
    params.output.history_points.coords = coords
    params.oper.max.hist = len(coords) + 1

    sim = Simul(params)
    sim.output.write_snakemake_config(custom_env_vars={"FOO": 1})

    with unset_snek_debug():
        if not sim.make.exec("compile"):
            build_log = Path(sim.output.path_run) / "build.log"
            log_matches(build_log, levels=["Error"])
            raise RuntimeError("cbox compilation failed")

    print("launching simulation with run_fg...")
    ok = sim.make.exec("run_fg", nproc=2)
    print("content of cbox.log after run_fg:")
    with open(Path(sim.output.path_run) / "cbox.log") as file:
        print(file.read())
    if not ok:
        raise RuntimeError("cbox simulation failed")

    path_run = Path(sim.output.path_run)
    print(
        f"Testing simulation done in {path_run}\nFiles:\n"
        f"{pformat(sorted(p.name for p in path_run.glob('*')))}\n"
        "Files in session_00:\n"
        f"{pformat(sorted(p.name for p in (path_run / 'session_00').glob('*')))}"
    )

    return sim
