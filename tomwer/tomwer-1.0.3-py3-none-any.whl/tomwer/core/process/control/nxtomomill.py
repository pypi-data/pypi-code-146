# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
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
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "30/07/2020"


from tomwer.core.process.task import TaskWithProgress
from tomwer.core.process.task import Task
from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from nxtomomill import converter as nxtomomill_converter
from nxtomomill.io.config import TomoHDF5Config as HDF5Config
from nxtomomill.io.config import TomoEDFConfig as EDFConfig

import os
import logging

_logger = logging.getLogger(__name__)


class H5ToNxProcess(Task, input_names=("data",), output_names=("data",)):
    """
    Process to convert from a bliss dataset to a nexus compliant dataset
    """

    @staticmethod
    def deduce_output_file_path(master_file_name, entry, outputdir=None):
        if outputdir is not None:
            file_dir = outputdir
        else:
            file_dir = os.path.dirname(master_file_name)
        file_name = os.path.basename(master_file_name)
        if "." in file_name:
            file_name = "".join(file_name.split(".")[:-1])

        entry_for_file_name = entry.lstrip("/")
        entry_for_file_name = entry_for_file_name.replace("/", "_")
        entry_for_file_name = entry_for_file_name.replace(".", "_")
        entry_for_file_name = entry_for_file_name.replace(":", "_")
        output_file_name = "_".join(
            (os.path.splitext(file_name)[0], entry_for_file_name + ".nx")
        )
        return os.path.join(file_dir, output_file_name)

    def run(self):
        scan = self.inputs.data
        if scan is None:
            self.outputs.data = None
            return

        _logger.processStarted("Start translate {} to NXTomo".format(str(scan)))
        if isinstance(scan, dict):
            scan = BlissScan.from_dict(scan)

        if not isinstance(scan, BlissScan):
            raise TypeError("Scan is expected to be an instance of BlissScan")
        output_file_path = self.deduce_output_file_path(
            master_file_name=scan.master_file, entry=scan.entry
        )
        _logger.info(" ".join(("write", str(scan), "to", output_file_path)))
        try:
            configuration = HDF5Config.from_dict(self.get_configuration())
            configuration.input_file = scan.master_file
            configuration.output_file = output_file_path
            configuration.entries = (scan.entry,)
            # overwrite some parameters
            configuration.single_file = False
            configuration.overwrite = True
            configuration.file_extension = ".nx"
            # ceinture et bretelle. Even if the file has only one
            # entry enforce creating a sub file.
            # Because at time T we might have only one file and then
            # at T+1 we might have another one. Just want to be safe here
            if hasattr(configuration, "bam_single_file"):
                configuration.bam_single_file = True
            convs = nxtomomill_converter.from_h5_to_nx(
                configuration=configuration,
            )
        except Exception as e:
            _logger.processFailed(
                "Fail to convert from bliss file: %s to NXTomo."
                "Conversion error is: %s" % (scan.master_file, e)
            )
            self.outputs.data = None
            return
        else:
            for conv in convs:
                conv_file, conv_entry = conv
                scan_converted = HDF5TomoScan(scan=conv_file, entry=conv_entry)
                _logger.processSucceed(
                    "{} has been translated to {}"
                    "".format(str(scan), str(scan_converted))
                )
                self.outputs.data = scan_converted

    def set_configuration(self, configuration):
        # for now the NXProcess cannot be tune
        if isinstance(configuration, HDF5Config):
            self._settings = configuration.to_dict()
        elif isinstance(configuration, dict):
            self._settings = configuration
        else:
            raise TypeError("invalid type: {}".format(type(configuration)))


class EDFToNxProcess(
    TaskWithProgress,
    input_names=("edf_to_nx_configuration",),
    optional_input_names=("progress", "edf_scan"),
    output_names=("data",),
):
    """
    Task calling edf2nx in order to insure conversion from .edf to .nx (create one NXtomo to be used elsewhere)
    """

    def run(self):
        config = self.inputs.edf_to_nx_configuration
        if isinstance(config, dict):
            config = EDFConfig.from_dict(config)
        elif not isinstance(config, EDFConfig):
            raise TypeError(
                "edf_to_nx_configuration should be a dict or an instance of {TomoEDFConfig}"
            )
        file_path, entry = nxtomomill_converter.from_edf_to_nx(
            configuration=config, progress=self.progress
        )
        self.outputs.data = HDF5TomoScan(entry=entry, scan=file_path)

    @staticmethod
    def deduce_output_file_path(folder_path, output_dir):
        if output_dir is None:
            output_dir = os.path.dirname(folder_path)

        return os.path.join(output_dir, os.path.basename(folder_path) + ".nx")
