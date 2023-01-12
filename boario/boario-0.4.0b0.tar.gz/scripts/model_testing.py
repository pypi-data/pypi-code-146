import os
import re
import sys
import itertools
import boario.simulation as sim
from boario.indicators import Indicators
from boario.event import Event
import json
import pathlib
import numpy as np
import pandas as pd

base_time = 1

# We instantiate a dictionary with the parameters
# (it is also possible to use a json file)
params = {
    # The name of the working directory to use (relative to current wd)
    "input_dir": "/home/sjuhel/Nextcloud/Thesis/Workbench/Data/BoARIO-inputs/",
    "output_dir": "/home/sjuhel/Nextcloud/Thesis/Workbench/Data/BoARIO-testing/dev-testing-new-shocks",
    # The directory to use to store results (relative to storage_dir)
    # i.e. here, the model will look for files in ~/boario/storage/ and
    # store results in ~/boario/storage/results/
    "results_storage": "results",
    # This tells the model to register the evolution of the stocks
    # of every industry (the file can be quite large (2Gbytes+ for
    # a 365 days simulation with exiobase))
    "register_stocks": False,
    "psi_param": 0.90,
    "order_type": "alt",
    "model_type": "ARIOPsi",
    "temporal_units_by_step": 1,
    "year_to_temporal_unit_factor": 365,
    "inventory_restoration_tau": 60,
    "alpha_base": 1.0,
    "alpha_max": 1.25,
    "alpha_tau": 365,
    "rebuild_tau": 60,
    "n_temporal_units_to_sim": 700,
    "impacted_region_base_production_toward_rebuilding": 0.0,
    "row_base_production_toward_rebuilding": 0.0,
   "mrio_params_file": "/home/sjuhel/Nextcloud/Thesis/Workbench/Data/BoARIO-inputs/builded-data/params/exiobase3_7_sectors_params.json"
}

#with open("/home/sjuhel/Nextcloud/Thesis/Workbench/Data/BoARIO-inputs/exps/experience-ciclad-parameters-explore-1/exiobase3_74_sectors_event_template.json") as f:
    #event = json.load(f)

with open("/home/sjuhel/Nextcloud/Thesis/Workbench/Data/BoARIO-inputs/builded-data/params/exiobase3_7_sectors_event_params.json") as f:
    event = json.load(f)

event["occur"] = 2
event["kapital_damage"] = 10000000000
event["q_dmg"] = event["kapital_damage"]
event["duration"] = 10
event["aff_sectors"] = ["Mining", "Manufacture"]
event["shock_type"] = "kapital_destroyed_rebuild"

event['dmg_distrib_regions'] = event['dmg_regional_distrib']
event['dmg_distrib_sectors_type'] = event['dmg_sectoral_distrib_type']
event['dmg_distrib_sectors'] = event['dmg_distrib_sectors_type']

event2 = event.copy()
event2["occur"] = 5
event2["aff_regions"] = ["DE"]

# We load the mrio table from a pickle file (created with the help of the
# pymrio module, more on that in the doc)
mrio_path = pathlib.Path("/home/sjuhel/Nextcloud/Thesis/Workbench/Data/BoARIO-inputs/builded-data/mrios/Exiobase/exiobase3_2011_7_sectors.pkl")

simul = sim.Simulation(params, mrio_path, modeltype="ARIOPsi")
simul.read_events_from_list([event])
simul.loop()
indic = Indicators.from_folder(
                           pathlib.Path(params['output_dir'])/params['results_storage'],
                           indexes_file=pathlib.Path(params['output_dir'])/params['results_storage']/"indexes.json",
                            include_crash=True)
indic.update_indicators()
indic.write_indicators()
