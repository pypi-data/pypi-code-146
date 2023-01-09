import random
import numpy as np
import pandas as pd
import pytest
import sys

import pycollimator as collimator
from pycollimator.error import NotFoundError

from tests import get_model_name


@pytest.mark.parametrize("name", ["test_001"])
def test_simulation_simple(name: str):
    model_name = get_model_name(name)
    model = collimator.load_model(model_name)
    assert model.name.startswith(model_name)

    sim = collimator.run_simulation(model, wait=False)
    assert isinstance(sim, collimator.simulations.Simulation)

    sim.wait()
    assert sim.status.lower() == "completed"

    # Get the results
    results = sim.results
    assert isinstance(results, collimator.simulations.SimulationResults)

    df = results.to_pandas()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

    # Get results data from the Test and Control output blocks
    test_output_blk = model.find_block("TestOutput")
    control_output_blk = model.find_block("ControlOutput")

    test_data = results[test_output_blk.name]
    control_data = results[control_output_blk.name]
    assert len(test_data) == len(control_data)
    assert len(test_data) > 0

    # Verify numerical results
    test_data = test_data.to_numpy()
    control_data = control_data.to_numpy()
    assert np.isclose(test_data, control_data).all()


# TODO: clean this up. there's test_configs which has some overlap
@pytest.mark.xfail(reason="Simulation-time configuration is not implemented yet")
@pytest.mark.parametrize("name", ["test_001"])
def test_simulation_configuration(name: str):
    model_name = get_model_name(name)
    model = collimator.load_model(model_name)

    stop_time = model.configuration.stop_time * 0.5
    configuration = {"stop_time": stop_time}
    sim = collimator.run_simulation(model, configuration=configuration, wait=True)
    assert sim.status.lower() == "completed"

    results = sim.results
    df = results.to_pandas()
    assert len(df["TestOutput.out_0"]) > 0

    # Check that we ran to the specified stop time
    assert np.isclose(df["TestOutput.out_0"].index[-1], stop_time)


@pytest.mark.parametrize("name", ["test_002"])
def test_simulation_parameters(name: str):
    model_name = get_model_name(name)
    model = collimator.load_model(model_name)

    assert len(model.get_parameters().keys()) > 0
    old_value = model.parameters["ParamValue"].value

    # Set param with dict access
    new_value = random.random()
    model.parameters["ParamValue"] = new_value

    with pytest.raises(NotFoundError):
        model.parameters["NewParameter"]
    # Guard against accidental parameter creation
    with pytest.raises(NotFoundError):
        model.parameters["NewParameter"] = 0

    sim = collimator.run_simulation(model, wait=True)
    assert sim.status.lower() == "completed"

    # Check the parameter value did not change: parameters aren't supposed to be changed
    model.reload()
    assert model.parameters["ParamValue"].value == old_value

    results = sim.results
    df = results.to_pandas()
    assert len(df["TestOutput.out_0"]) > 0

    # Check that the constant block has the right value
    expected_result = np.array([new_value] * len(df["TestOutput.out_0"]))
    assert np.isclose(df["TestOutput.out_0"], expected_result).all()

    # Set param with method
    new_value = random.random()
    model.set_parameters({"ParamValue": new_value})

    sim = collimator.run_simulation(model, wait=True)
    assert sim.status.lower() == "completed"

    # Check the parameter value did not change: parameters aren't supposed to be changed
    model.reload()
    assert model.parameters["ParamValue"].value == old_value

    results = sim.results
    df = results.to_pandas()
    assert len(df["TestOutput.out_0"]) > 0

    # Check that the constant block has the right value
    expected_result = np.array([new_value] * len(df["TestOutput.out_0"]))
    assert np.isclose(df["TestOutput.out_0"], expected_result).all()

    # Set param and save to model
    new_value = random.random()
    model.set_parameters({"ParamValue": new_value}, save=True)

    sim = collimator.run_simulation(model, wait=True)
    assert sim.status.lower() == "completed"

    # Check the parameter value updated
    model.reload()
    assert model.parameters["ParamValue"].value == new_value

    results = sim.results
    df = results.to_pandas()
    assert len(df["TestOutput.out_0"]) > 0

    # Check that the constant block has the right value
    expected_result = np.array([new_value] * len(df["TestOutput.out_0"]))
    assert np.isclose(df["TestOutput.out_0"], expected_result).all()


@pytest.mark.parametrize("name", ["test_005"])
def test_configs(name: str):
    model_name = get_model_name(name)
    model = collimator.load_model(model_name)

    # Set a config with property setter
    original_stop_time = model.configuration.stop_time
    new_stop_time_1 = original_stop_time + 1
    model.configuration.stop_time = new_stop_time_1
    assert model.configuration.stop_time == new_stop_time_1

    sim = collimator.run_simulation(model, wait=True)
    assert sim.status.lower() == "completed"
    assert sim.results.to_pandas().index[-1] == new_stop_time_1

    # Set a config with method
    new_stop_time_2 = original_stop_time + 2
    model.set_configuration({"stop_time": new_stop_time_2})
    assert model.configuration.stop_time == new_stop_time_2

    sim = collimator.run_simulation(model, wait=True)
    assert sim.status.lower() == "completed"
    assert sim.results.to_pandas().index[-1] == new_stop_time_2

    # Model configs are preserved by default
    original_model = collimator.load_model(model_name)
    assert original_model.configuration.stop_time == original_stop_time


@pytest.mark.parametrize("name", ["test_002"])
def test_stop_simulation(name: str):
    model_name = get_model_name(name)
    model = collimator.load_model(model_name)

    sim = collimator.run_simulation(model, wait=False)
    sim.stop()


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
