#!/bin/env python
"""
Generate a VTF like 214 dataset based on some CRISP data.

To run this example you need the input crisp file which should have one HDU
with shape (980, 966, 19, 4, 128).

Usage
-----

vtf_crisp_5d.py <input_filename> <output_directory>
"""
import sys
from pathlib import Path

from dkist_inventory.asdf_generator import dataset_from_fits

from dkist_data_simulator.examples.vtf_crisp_5d import VTFCRISP5DDataset

# Modify these with a path if you don't want to run this as a script.
input_file = Path(sys.argv[1])
output_dir = Path(sys.argv[2])

# Set n_repeats to a lower number to make a smaller dataset. 5 is a good small value.
ds = VTFCRISP5DDataset(input_file, n_repeats=5)

ds.generate_files(
    output_dir,
    filename_template="{ds.index:05d}.fits",
    expected_only=False,
    progress_bar=True,
)
dataset_from_fits(output_dir, "vtf_crisp_5d.asdf", relative_to=output_dir)
