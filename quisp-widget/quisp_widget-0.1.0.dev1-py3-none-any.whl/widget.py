#!/usr/bin/env python
# coding: utf-8

# Copyright (c) zigen.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget, CallbackDispatcher
from traitlets import Unicode
from ._frontend import module_name, module_version


class QuispWidget(DOMWidget):
    """TODO: Add docstring here"""

    _model_name = Unicode("QuispIFrameModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("QuispIFrameView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Unicode("Hello World").tag(sync=True)

    def __init__(self):
        super().__init__()
        self.layout.width = "100%"
        self.jsonl = None
        self.output = None
        self.on_msg(self.callback, remove=False)

    def callback(self, widget, content, buffers):
        if 'jsonl' in content:
            self.jsonl = content['jsonl']
        if 'output' in content:
            self.output= content['output']


    def run(self):
        self.send({"msg": "runNormal"})

    def runStep(self):
        self.send({"msg": "runStep"})

    def runFast(self):
        self.send({"msg": "runFast"})

    def stop(self):
        self.send({"msg": "stop"})

    def load(self, network):
        inifile = self.generate_ini_file(network.name)
        self.send({"msg": "load", "ned": network.dump(), "ini": inifile})

    def readResult(self):
        self.send({"msg": "readResult"})

    def generate_ini_file(self, network_name: str) -> str:
        config_name = "Custom"
        return f"""
[General]
seed-set = \\${{runnumber}}
sim-time-limit = 100s

image-path = "./quisp/images"
**.logger.log_filename = "/result.jsonl"
**.tomography_output_filename = "/result.output"
**.speed_of_light_in_fiber = 205336.986301 km

**.h_gate_error_rate = 1/2000
**.h_gate_x_error_ratio = 0
**.h_gate_y_error_ratio = 0
**.h_gate_z_error_ratio = 0

**.Measurement_error_rate = 1/2000
**.Measurement_x_error_ratio = 1
**.Measurement_y_error_ratio = 1
**.Measurement_z_error_ratio = 1

**.x_gate_error_rate = 1/2000
**.x_gate_x_error_ratio = 0
**.x_gate_y_error_ratio = 0
**.x_gate_z_error_ratio = 0

**.z_gate_error_rate = 1/2000
**.z_gate_x_error_ratio = 0
**.z_gate_y_error_ratio = 0
**.z_gate_z_error_ratio = 0


#Error on Target, Error on Controlled
**.cnot_gate_error_rate = 1/2000
**.cnot_gate_iz_error_ratio = 1
**.cnot_gate_zi_error_ratio = 1
**.cnot_gate_zz_error_ratio = 1
**.cnot_gate_ix_error_ratio = 1
**.cnot_gate_xi_error_ratio = 1
**.cnot_gate_xx_error_ratio = 1
**.cnot_gate_iy_error_ratio = 1
**.cnot_gate_yi_error_ratio = 1
**.cnot_gate_yy_error_ratio = 1

**.memory_x_error_rate = 1.11111111e-7
**.memory_y_error_rate = 1.11111111e-7
**.memory_z_error_rate = 1.11111111e-7
**.memory_energy_excitation_rate = 0.000198
**.memory_energy_relaxation_rate = 0.00000198
**.memory_completely_mixed_rate = 0

# when to start the BSA timing notification.
**.initial_notification_timing_buffer = 10 s
**.TrafficPattern = 1
**.LoneInitiatorAddress = 1

[Config {config_name}]
network = networks.{network_name}
seed-set = 0
**.number_of_bellpair = 7000
**.buffers = 100



**.emission_success_probability = 0.46*0.49

# Error on optical qubit in a channel
**.channel_loss_rate = 0.04500741397 # per km. 1 - 10^(-0.2/10)
**.channel_x_error_rate = 0.01
**.channel_z_error_rate = 0.01
**.channel_y_error_rate = 0.01

# Internal HOM in QNIC
**.internal_hom_loss_rate = 0
**.internal_hom_error_rate = 0 #Not inplemented
**.internal_hom_required_precision = 1.5e-9 #Schuck et al., PRL 96,
**.internal_hom_photon_detection_per_sec = 1000000000
**.internal_hom_darkcount_probability = 10e-8 #10/s * 10^-9

#Stand-alone HOM in the network
**.hom_loss_rate = 0
**.hom_error_rate = 0 #Not inplemented
**.hom_required_precision = 1.5e-9 #Schuck et al., PRL 96,
**.hom_photon_detection_per_sec = 1000000000
**.hom_darkcount_probability = 10e-8 #1%

**.link_tomography = false
**.EndToEndConnection = true
**.initial_purification = 2
**.purification_type = 1001
"""
