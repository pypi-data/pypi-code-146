import sys

import numpy as np
import pandas as pd
import pytest


import pycollimator as collimator
from pycollimator.diagrams import DataSourceBlock

from tests import get_model_name


@pytest.mark.parametrize("name", ["test_003"])
def test_datasource_simple(name: str):
    model_name = get_model_name(name)
    model = collimator.load_model(model_name)

    # Check that the simulation can't run without a valid datasource input
    sim = collimator.run_simulation(model, wait=True)
    assert sim.status.lower() == "failed"

    # 10+1 random points at 0.1s intervals
    test_data = np.random.rand(11)
    test_times = np.linspace(0, 1.0, len(test_data))
    test_df = pd.DataFrame(test_data, index=test_times, columns=["value"])

    block: DataSourceBlock = model.find_block("DataSourceBlock")
    assert isinstance(block, DataSourceBlock)

    block_sampling_interval = block.get_parameter("sampling_interval")
    print("block sampling interval", block_sampling_interval, type(block_sampling_interval))
    assert np.isclose(block_sampling_interval, 0.1)

    print("block data set to", test_df)
    block.set_data(test_df)

    # Interpolation is set to a higher value that
    configuration = {"stop_time": 1.0, "discrete_step": 0.1, "interpolation": 10.0}
    model.set_configuration(configuration)

    sim = collimator.run_simulation(model, wait=True)
    df = sim.results.to_pandas()

    # TestOutput is a ZOH block used to ensure that the DataSource block is read as a discrete block
    print(df)
    assert len(df["TestOutput.out_1"]) > 0
    assert np.isclose(df["TestOutput.out_1"], test_data).all()


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
