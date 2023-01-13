import os
import sys
# noinspection PyPackageRequirements
import json

cur_file_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = f'{cur_file_dir}/../fabrique_nodes_core'
sys.path.append(lib_dir)
os.chdir(cur_file_dir)

import tests.import_spoofer as import_spoofer  # noqa: F401

import fabrique_nodes_core.configs_model as configs_model


def file2str(pth):
    with open(pth) as fp:
        txt = fp.read()
    return txt


actor_data = json.loads(file2str(f'{cur_file_dir}/data/fab_proj.json'))


def cfg2model(cfg_dict):
    cfg = configs_model.Model(**cfg_dict)
    outputs = {int(k): {key: val.connections for key, val in v.outputs.items()} for k, v in cfg.nodes.items()}
    inputs = {int(k): {key: val.connections for key, val in v.inputs.items()} for k, v in cfg.nodes.items()}
    cfg_data = {int(k): v.data for k, v in cfg.__dict__['nodes'].items()}
    return cfg, outputs, inputs, cfg_data


def test_cfg_model():
    _, outputs, inputs, cfg_data = cfg2model(actor_data)
    assert len(outputs) == 5
    assert len(inputs) == 5
    assert len(cfg_data) == 5
