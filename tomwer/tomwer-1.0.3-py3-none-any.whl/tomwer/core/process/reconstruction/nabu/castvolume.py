# coding: utf-8
###########################################################################
# Copyright (C) 2016 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################

"""
This module is dedicated to cast of volume from one file format to the other.
"""

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "15/12/2021"


import os
import inspect
from processview.core.superviseprocess import SuperviseProcess
from tomwer.core.cluster.cluster import SlurmClusterConfiguration
from tomwer.core.process.reconstruction.nabu import settings
from tomwer.core.process.task import Task
from tomwer.core.process.reconstruction.nabu.nabucommon import (
    NabuOutputFileFormat,
)
from processview.core.manager import ProcessManager, DatasetState
import numpy
import logging
from tomoscan.volumebase import VolumeBase
from nabu.io.cast_volume import (
    cast_volume as _nabu_cast_volume,
    RESCALE_MIN_PERCENTILE,
    RESCALE_MAX_PERCENTILE,
    get_default_output_volume,
)
from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.utils.slurm import get_slurm_script_name
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.core.volume.volumebase import TomwerVolumeBase
from sluurp.job import SBatchScriptJob
from sluurp.executor import submit as submit_to_slurm_cluster

_logger = logging.getLogger(__name__)


DEFAULT_OUTPUT_DIR = "{volume_data_parent_folder}/cast_volume"


class CastVolumeTask(
    Task,
    SuperviseProcess,
    input_names=(
        "volume",
        "configuration",
    ),
    optional_input_names=("scan", "output_volume"),
    output_names=(
        "volume",
        "future_tomo_obj",
    ),
):
    def __init__(
        self,
        process_id=None,
        varinfo=None,
        inputs=None,
        node_id=None,
        node_attrs=None,
        execinfo=None,
    ):
        SuperviseProcess.__init__(self, process_id=process_id)
        Task.__init__(
            self,
            varinfo=varinfo,
            inputs=inputs,
            node_id=node_id,
            node_attrs=node_attrs,
            execinfo=execinfo,
        )
        self._cluster_config = None

    def run(self):
        input_volume = self.inputs.volume
        if not isinstance(input_volume, VolumeBase):
            raise TypeError(
                f"input_volume is a {type(input_volume)} when {VolumeBase} expected"
            )
        configuration = self.inputs.configuration
        self._cluster_config = configuration.pop("cluster_config", None)
        if isinstance(self._cluster_config, SlurmClusterConfiguration):
            self._cluster_config = self._cluster_config.to_dict()
        if self.inputs.scan:
            scan = self.inputs.scan
        else:
            scan = None
        if self.inputs.output_volume:
            output_volume = self.inputs.output_volume
            if not isinstance(output_volume, TomwerVolumeBase):
                output_volume = VolumeFactory.create_tomo_object_from_identifier(
                    output_volume
                )
        else:
            output_data_type = configuration.get(
                "output_type", None
            )  # expects values like hdf5, edf ...
            output_dir = configuration.get("output_dir", None)
            if output_data_type is None or output_dir is None:
                mess = "'output_volume' or ('output_type' and 'output_dir' from configuraiton) should be provided."
                _logger.processFailed(f"volume cast of {str(input_volume)} failed")
                ProcessManager().notify_dataset_state(
                    dataset=input_volume,
                    process=self,
                    state=DatasetState.FAILED,
                )
                raise ValueError(mess)

            output_dir = TomwerVolumeBase.format_output_location(
                location=output_dir,
                volume=input_volume,
            )

            output_volume = get_default_output_volume(
                input_volume=input_volume,
                output_type=NabuOutputFileFormat.from_value(output_data_type).value,
                output_dir=output_dir,
            )
            # convert from tomoscan volume to tomwer volume
            output_volume = VolumeFactory.create_tomo_object_from_identifier(
                output_volume.get_identifier().to_str()
            )

        # build output volume object
        overwrite = configuration.get("overwrite", False)
        output_volume.overwrite = overwrite

        output_data_type = numpy.dtype(
            configuration.get("output_data_type")
        )  # expects values like numpy uint8, unint16...

        rescale_min_percentile = configuration.get(
            "rescale_min_percentile", RESCALE_MIN_PERCENTILE
        )
        rescale_max_percentile = configuration.get(
            "rescale_max_percentile", RESCALE_MAX_PERCENTILE
        )
        data_min = configuration.get("data_min", None)
        data_max = configuration.get("data_max", None)

        # run volume cast locally
        if self._cluster_config is None:
            cast_params = {
                "input_volume": input_volume,
                "output_volume": output_volume,
                "output_data_type": output_data_type,
                "data_min": data_min,
                "data_max": data_max,
                "scan": scan,
                "rescale_min_percentile": rescale_min_percentile,
                "rescale_max_percentile": rescale_max_percentile,
            }
            if "overwrite" in inspect.signature(_nabu_cast_volume).parameters:
                cast_params["overwrite"] = overwrite
            try:
                volume = _nabu_cast_volume(**cast_params)
            except Exception as e:
                mess = f"volume cast of {str(input_volume)} failed. Reason is {str(e)}"
                _logger.processFailed(mess)
                state = DatasetState.FAILED

            else:
                try:
                    volume.save()
                except Exception as e:
                    mess = f"fail to save cast volume {str(output_volume)}. Reason is {str(e)}"
                    _logger.processFailed(mess)
                    state = DatasetState.FAILED
                else:
                    mess = f"volume cast of {str(input_volume)} succeed"
                    _logger.processSucceed(mess)
                    state = DatasetState.SUCCEED

            ProcessManager().notify_dataset_state(
                dataset=input_volume,
                process=self,
                state=state,
                details=mess,
            )
            self.outputs.future_tomo_obj = None
            self.outputs.volume = output_volume
        # run volume cast remotly
        else:

            def get_command():
                command = f"python3 -m {settings.NABU_CAST_APP_PATH} '{input_volume.get_identifier().to_str()}'"
                command += (
                    f" --output_volume='{output_volume.get_identifier().to_str()}'"
                )
                if overwrite:
                    command += " --overwrite"
                command += f" --output_type={str(output_data_type)}"
                if data_min is not None:
                    command += f" --data_min={data_min}"
                if data_max is not None:
                    command += f" --data_max={data_max}"
                if rescale_min_percentile is not None:
                    command += f" --rescale_min_percentile={rescale_min_percentile}"
                if rescale_max_percentile is not None:
                    command += f" --rescale_max_percentile={rescale_max_percentile}"

                return command

            script_name = get_slurm_script_name(prefix="nabu_cast")
            if scan is not None:
                working_directory = scan.working_directory
                script_path = os.path.join(scan.path, "slurm_scripts", script_name)
            else:
                working_directory = os.path.dirname(input_volume.data_url.file_path())
                script_path = os.path.join(
                    working_directory, "slurm_scripts", script_name
                )
            # for now force job name
            self._cluster_config[
                "job_name"
            ] = f"tomwer-cast-volume {input_volume.get_identifier().to_str()} to {output_volume.get_identifier().to_str()}"
            job = SBatchScriptJob(
                slurm_config=self._cluster_config,
                script=(get_command(),),
                script_path=script_path,
                clean_script=False,
                working_directory=working_directory,
            )
            future_slurm_job = submit_to_slurm_cluster(job)
            if scan is not None:
                future_obj = scan
            else:
                future_obj = output_volume
            self.outputs.future_tomo_obj = FutureTomwerObject(
                tomo_obj=future_obj,
                futures=(future_slurm_job,),
                process_requester_id=self.process_id,
            )
            self.outputs.volume = output_volume
