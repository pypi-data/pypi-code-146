import pytest
import sys

import numpy as np

import pycollimator as collimator
from pycollimator.error import NotFoundError, CollimatorApiError

from tests import get_model_name


@pytest.mark.parametrize("name", ["test_004"])
def test_slice_results_by_path(name: str):
    model_name = get_model_name(name)
    model = collimator.load_model(model_name)

    sim = collimator.run_simulation(model, wait=True)
    assert sim.status.lower() == "completed"

    results = sim.get_results()
    df = results.to_pandas()
    assert len(df.columns) == 13

    with pytest.raises(NotFoundError):
        results["path that does not exist"]
    with pytest.raises(NotFoundError):
        results.to_pandas("path that does not exist")

    # Read columns from data frame
    adder_full_path = "Group_1.Group_0.SquareRoot_0.out_0"
    assert len(df[adder_full_path]) > 0

    top_level_group_full_path = "Group_1.Outport_0"
    assert len(df[top_level_group_full_path]) > 0

    # Dataframe doesn't recognize paths without ports but results do.
    top_level_group = "Group_1"
    assert len(results[top_level_group]) > 0

    nested_group = "Group_1.Group_0"
    assert len(results[nested_group]) > 0

    # Check find by type constructs path correctly
    sqrt = sim.model.find_block(type="SquareRoot")
    assert sqrt.path == "Group_1.Group_0.SquareRoot_0"
    assert len(results[sqrt]) > 0

    # All columns from the dataframe should be in the results
    for col in results.columns:
        assert len(results[col]) > 0


@pytest.mark.parametrize("name", ["test_004"])
def test_request_results_by_path(name: str):
    model_name = get_model_name(name)
    model = collimator.load_model(model_name)

    sim = collimator.run_simulation(model, wait=True)
    assert sim.status.lower() == "completed"

    base_results = sim.get_results().to_pandas()
    assert len(base_results.columns) == 13

    # Request specific signal data as single string
    adder_full_path = "Group_1.Group_0.SquareRoot_0.out_0"
    top_level_group_full_path = "Group_1.Outport_0"

    results = sim.get_results(adder_full_path).to_pandas()
    assert results.columns.values.tolist() == [adder_full_path]
    assert np.isclose(results[adder_full_path], base_results[adder_full_path]).all()

    results = sim.get_results(top_level_group_full_path).to_pandas()
    assert results.columns.values.tolist() == [top_level_group_full_path]
    assert np.isclose(results[top_level_group_full_path], base_results[top_level_group_full_path]).all()

    # Request single path
    results = sim.get_results([top_level_group_full_path]).to_pandas()
    assert results.columns.values.tolist() == [top_level_group_full_path]
    assert np.isclose(results[top_level_group_full_path], base_results[top_level_group_full_path]).all()

    # Request data for multiple signals
    multiple_signals = [adder_full_path, top_level_group_full_path]
    results = sim.get_results(multiple_signals).to_pandas()
    assert results.columns.values.tolist() == multiple_signals
    assert np.isclose(results[adder_full_path], base_results[adder_full_path]).all()
    assert np.isclose(results[top_level_group_full_path], base_results[top_level_group_full_path]).all()

    # Raise error for invalid signal path
    with pytest.raises(CollimatorApiError):
        results = sim.get_results(["path that does not exist"])
    # Raise error if there is any invalid signal path
    with pytest.raises(CollimatorApiError):
        results = sim.get_results([*multiple_signals, "path that does not exist"])


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
