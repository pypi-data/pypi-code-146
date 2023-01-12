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

"""contain utils for score process
"""

__authors__ = [
    "H.Payno",
]
__license__ = "MIT"
__date__ = "27/10/2021"


from tomwer.core.cluster.cluster import (
    SlurmClusterConfiguration,
)
from sluurp.executor import submit as submit_to_slurm_cluster
from sluurp.job import SBatchScriptJob
from tomwer.core.process.reconstruction.nabu.target import Target
from tomwer.core.process.reconstruction.nabu.utils import (
    _NabuPhaseMethod,
    nabu_std_err_has_error,
)
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.utils.slurm import get_slurm_script_name, is_slurm_available
from tomwer.core.process.reconstruction.normalization.params import (
    _ValueSource as INormSource,
)
from tomoscan.normalization import Method as INormMethod
from silx.utils.enum import Enum as _Enum
from silx.io.url import DataUrl
from typing import Iterable, Optional
from typing import Union
import logging
import subprocess
from . import settings
from . import utils
import os
import uuid
from tomoscan.io import HDF5File
import numpy

_logger = logging.getLogger(__name__)
try:
    from nabu.pipeline.fullfield.local_reconstruction import (  # noqa F401
        ChunkedReconstructor,
    )
except (ImportError, OSError) as e:
    # import of cufft library can bring an OSError if cuda not install
    _logger.error(e)
    has_nabu = False
else:
    has_nabu = True


class NabuOutputFileFormat(_Enum):
    TIFF = "tiff"
    HDF5 = "hdf5"
    JP2K = "jp2"
    EDF = "edf"
    RAW = "vol"

    @classmethod
    def from_value(cls, value):
        if isinstance(value, str):
            value = value.lstrip(".")
        return super().from_value(value)


def get_file_format(file_str):
    extension = os.path.splitext(file_str.lower())[-1]
    extension = extension.lstrip(".")
    if extension in ("tiff", "tif"):
        return NabuOutputFileFormat.TIFF
    elif extension in ("hdf5", "hdf", "h5"):
        return NabuOutputFileFormat.HDF5
    elif extension in ("jp2", "jp2k", "jpg2k"):
        return NabuOutputFileFormat.JP2K
    elif extension in ("edf",):
        return NabuOutputFileFormat.EDF
    elif extension in ("vol", "raw"):
        return NabuOutputFileFormat.RAW
    else:
        raise ValueError(f"Unrecognized file extension {extension} from {file_str}")


class ResultsRun:
    """
    Base class of results for nabu
    """

    def __init__(self, success, config) -> None:
        self.__success = success
        self.__config = config

    @property
    def success(self) -> bool:
        return self.__success

    @property
    def config(self) -> dict:
        return self.__config

    def __str__(self) -> str:
        return f"result from nabu run: {'succeed' if self.success else 'failed'} with \n - config:{self.config} \n"


class ResultsWithStd(ResultsRun):
    """Nabu result with std"""

    def __init__(self, std_out, std_err, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__std_err = std_err
        self.__std_out = std_out

    @property
    def std_out(self) -> str:
        return self.__std_out

    @property
    def std_err(self) -> str:
        return self.__std_err

    def __str__(self) -> str:
        res = super().__str__()
        res += f"\n {self.std_out} \n {self.std_err}"
        return res


class ResultsLocalRun(ResultsWithStd):
    """Nabu result when run locally.
    If this is the case we should be able to retrieve directly the results urls"""

    def __init__(
        self,
        results_urls: tuple,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if not isinstance(results_urls, Iterable):
            raise TypeError(
                f"results_urls is expected to be an Iterable not {type(results_urls)}"
            )
        self.__results_urls = results_urls

    @property
    def results_urls(self) -> tuple:
        return self.__results_urls

    def __str__(self) -> str:
        res = super().__str__()
        res += f"\n - result urls: {self.results_urls}"
        return res


class ResultSlurmRun(ResultsWithStd):
    """Nabu result when run on slurm. on this case we expect to get a future and a distributed client"""

    def __init__(
        self,
        future_slurm_jobs: tuple,
        job_id: Optional[int],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.__future_slurm_jobs = future_slurm_jobs
        self.__job_id = job_id

    @property
    def future_slurm_jobs(self):
        return self.__future_slurm_jobs

    @property
    def job_id(self) -> Optional[int]:
        return self.__job_id

    def __str__(self) -> str:
        res = super().__str__()
        res += f"\n - future job slurms: {self.future_slurm_jobs} \n"
        return res


class _NabuBaseReconstructor:
    """
    Base class to submit a job to nabu
    """

    TIMEOUT_SLURM_JOB_SUBMISSION = 30
    """Timeout when submit a job to slurm cluster. In second"""

    EXPECTS_SINGLE_SLICE = True

    def __init__(
        self,
        scan: TomwerScanBase,
        dry_run: bool,
        target: Target,
        cluster_config: Optional[Union[dict, SlurmClusterConfiguration]],
        process_name: str,
    ) -> None:
        self._scan = scan
        self._target = Target.from_value(target)
        self._dry_run = dry_run
        self._process_name = process_name
        if isinstance(cluster_config, SlurmClusterConfiguration):
            self._cluster_config = cluster_config
        elif isinstance(cluster_config, dict):
            self._cluster_config = SlurmClusterConfiguration.from_dict(cluster_config)
        elif cluster_config is None:
            self._cluster_config = None
        else:
            raise TypeError(
                f"cluster config is expected to be a dict or an instance of {SlurmClusterConfiguration}. Not {type(cluster_config)}"
            )

    @property
    def scan(self):
        return self._scan

    @property
    def target(self):
        return self._target

    @property
    def cluster_config(self):
        return self._cluster_config

    @property
    def dry_run(self):
        return self._dry_run

    @property
    def process_name(self):
        return self._process_name

    def only_create_config_file(self):
        """Should we run the reconstruction or only create the configuration file"""
        return False

    def run(self) -> Iterable:
        """
        run the requested slices.

        :return: Iterable of ResultsRun.
        """
        raise NotImplementedError("Base class")

    def _process_config(
        self,
        config_to_dump: dict,
        config_file: str,
        file_format: str,
        start_z: Optional[int],
        end_z: Optional[int],
        info: Optional[str],
        process_name: str,
    ):
        """
        process provided configuration

        :param str info:
        """
        if self.dry_run is True or self.only_create_config_file():
            return ResultsRun(
                success=True,
                config=config_to_dump,
            )
        elif self.target is Target.LOCAL:
            _logger.info(f"run {info} for {self.scan} with {config_to_dump}")
            return self._run_nabu_locally(
                conf_file=config_file,
                file_format=file_format,
                config_to_dump=config_to_dump,
                start_z=start_z,
                end_z=end_z,
            )
        elif self.target is Target.SLURM:
            _logger.info(
                f"run {info} on slurm for {self.scan.path} with {config_to_dump}"
            )
            return self._run_nabu_on_slurm(
                conf_file=config_file,
                config_to_dump=config_to_dump,
                cluster_config=self.cluster_config.to_dict(),
                start_z=start_z,
                end_z=end_z,
                process_name=process_name,
                info=info,
            )
        else:
            raise ValueError(f"{self.target} is not recognized as a valid target")

    def _run_nabu_locally(
        self,
        conf_file: str,
        file_format: str,
        config_to_dump: dict,
        start_z: int,
        end_z: int,
    ) -> ResultsLocalRun:
        """
        run locally nabu for a single configuration file.

        :param str conf_file: path to the nabu .cfg file
        :param str file_format: format of the generated file
        :param dict config_to_dump: configuration saved in the .cfg as a dictionary
        :return: results of the local run
        :rtype: ResultsLocalRun
        """
        if not has_nabu:
            raise ImportError("Fail to import nabu")
        command = " ".join(
            ("python3", "-m", settings.NABU_FULL_FIELD_APP_PATH, conf_file)
        )
        _logger.info(f'call nabu from "{command}"')
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=self.scan.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        outs, errs = process.communicate()

        recons_urls = utils.get_recons_volume_identifier(
            file_prefix=config_to_dump["output"]["file_prefix"],
            location=config_to_dump["output"]["location"],
            slice_index=None,
            scan=self.scan,
            file_format=file_format,
            start_z=start_z,
            end_z=end_z,
            expects_single_slice=self.EXPECTS_SINGLE_SLICE,
        )
        return ResultsLocalRun(
            success=not nabu_std_err_has_error(errs),
            results_urls=recons_urls,
            std_out=outs,
            std_err=errs,
            config=config_to_dump,  # config_slices,
        )

    def _run_nabu_on_slurm(
        self,
        conf_file: str,
        config_to_dump: dict,
        cluster_config: dict,
        start_z: int,
        end_z: int,
        process_name: str,
        info: str,
    ) -> ResultSlurmRun:
        """
        Run a nabu reconstruction on slurm of a single configuration

        :return: results of the slurm run
        :rtype: ResultSlurmRun
        """
        if not isinstance(conf_file, str):
            raise TypeError(f"conf_file is expected to be a strg not {type(conf_file)}")
        if not isinstance(config_to_dump, dict):
            raise TypeError(
                f"config_to_dump is expected to be a strg not {type(config_to_dump)}"
            )
        if not is_slurm_available():
            raise RuntimeError("slurm not available")
        if not isinstance(cluster_config, dict):
            raise ValueError(
                f"cluster config is expected to be a dict not {type(cluster_config)}"
            )

        # create slurm cluster
        project_name = cluster_config.get(
            "job_name", "tomwer_{scan}_-_{process}_-_{info}"
        )
        project_name = project_name.format(
            scan=str(self.scan), process=process_name, info=info
        )
        # project name should not contain any spaces as it will be integrated in a script and interpreted.
        project_name = project_name.replace(" ", "_")
        cluster_config["job_name"] = project_name

        # submit job
        script_name = get_slurm_script_name(prefix="nabu")
        # for now force job name
        cluster_config["job_name"] = f"tomwer-nabu {conf_file}"
        job = SBatchScriptJob(
            slurm_config=cluster_config,
            script=(f"python3 -m {settings.NABU_FULL_FIELD_APP_PATH} {conf_file}",),
            script_path=os.path.join(self.scan.path, "slurm_scripts", script_name),
            clean_script=False,
            working_directory=self.scan.working_directory,
        )
        future_slurm_job = submit_to_slurm_cluster(job)

        callbacks = self._get_futures_slurm_callback(config_to_dump)
        assert isinstance(
            callbacks, tuple
        ), f"callbacks is expected to an instance of tuple and not {type(callbacks)}"
        for callback in callbacks:
            future_slurm_job.add_done_callback(callback.process)

        return ResultSlurmRun(
            success=True,
            config=config_to_dump,
            future_slurm_jobs=(future_slurm_job,),
            std_out=None,
            std_err=None,
            job_id=job.job_id,
        )

    def _get_futures_slurm_callback(self, config_to_dump) -> tuple:
        """Return a tuple a potential callback to be launch once the future is done"""
        return tuple()

    def _treateOutputSliceConfig(self, config):
        """
        - add or overwrite some parameters of the dictionary
        - create the output directory if does not exist
        """
        # handle phase
        pag = False
        db = None
        if "phase" in config:
            if (
                "method" in config["phase"]
                and config["phase"]["method"] == _NabuPhaseMethod.PAGANIN.value
            ):
                pag = True
                if "delta_beta" in config["phase"]:
                    db = round(float(config["phase"]["delta_beta"]))
        # handle output
        if "output" in config:
            _file_name = self._get_file_basename_reconstruction(pag=pag, db=db)
            config["output"]["file_prefix"] = _file_name
            location = config["output"].get("location", None)
            if location not in ("", None):
                location = self.format_output_location(location, scan=self.scan)
                # if user specify the location
                if not os.path.isdir(config["output"]["location"]):
                    os.makedirs(location)
            else:
                # otherwise default location will be the data root level
                location = self.scan.path
            config["output"]["location"] = location
        # handle preproc
        if "preproc" not in config:
            config["preproc"] = {}
        if self.scan.intensity_normalization.method is INormMethod.NONE:
            config["preproc"]["sino_normalization"] = ""
        else:
            config["preproc"][
                "sino_normalization"
            ] = self.scan.intensity_normalization.method.value

        extra_infos = self.scan.intensity_normalization.get_extra_infos()

        nabu_cfg_folders = os.path.join(
            config["output"]["location"], settings.NABU_CFG_FILE_FOLDER
        )
        os.makedirs(nabu_cfg_folders, exist_ok=True)

        # configuration file and nabu_tomwer_serving_hatch must be in the same folder
        serving_hatch_file = os.path.join(
            nabu_cfg_folders, settings.NABU_TOMWER_SERVING_HATCH
        )

        source = extra_infos.get("source", INormSource.NONE)
        source = INormSource.from_value(source)

        if source is INormSource.NONE:
            pass
        elif source is INormSource.MANUAL_SCALAR:
            if "value" not in extra_infos:
                raise KeyError(
                    "value should be provided in extra)infos for scalar defined manually"
                )
            else:
                # check if the dataset has already been saved once and if we can reuse it
                dataset_url = extra_infos.get("dataset_created_by_tomwer", None)
                if dataset_url is not None:
                    # if an url exists insure we can access it
                    dataset_url = DataUrl(path=dataset_url)
                    if os.path.exists(dataset_url.file_path()):
                        with HDF5File(
                            dataset_url.file_path(), mode="r", swmr="True"
                        ) as h5f:
                            if dataset_url.data_path() not in h5f:
                                dataset_url = None
                    else:
                        dataset_url = None
                # if unable toi reuse an existing url them dump the value
                if dataset_url is None:
                    value = extra_infos["value"]
                    if isinstance(value, (tuple, list)):
                        value = numpy.asarray(value)
                    dataset_url = dump_normalization_array_for_nabu(
                        scan=self.scan,
                        array=value,
                        output_file=serving_hatch_file,
                    )
                    extra_infos.update(
                        {"dataset_created_by_tomwer": dataset_url.path()}
                    )
                    self.scan.intensity_normalization.set_extra_infos(extra_infos)

                config["preproc"]["sino_normalization_file"] = dataset_url.path()
        elif source is INormSource.DATASET:
            url = extra_infos["dataset_url"]
            if isinstance(url, DataUrl):
                config["preproc"]["sino_normalization_file"] = url.path()
            elif isinstance(url, str):
                config["preproc"]["sino_normalization_file"] = url
            else:
                raise TypeError(
                    f"dataset_url is expected to be an instance of DataUrl or str representing a DataUrl. Not {type(url)}"
                )
        else:
            raise NotImplementedError(f"source type {source.value} is not handled")

        return config

    def _get_file_basename_reconstruction(self, pag, db):
        """return created file base name"""
        raise NotImplementedError("Base class")

    @staticmethod
    def format_output_location(location, scan: TomwerScanBase):
        """
        format possible keys from the location like {scan_dir} or {scan_path}

        :param location:
        :param scan:
        :return:
        """
        if scan is None:
            _logger.warning("scan is !none, enable to format the nabu output location")

        keywords = {
            "scan_dir_name": scan.scan_dir_name(),
            "scan_basename": scan.scan_basename(),
            "scan_parent_dir_basename": scan.scan_parent_dir_basename(),
        }
        for keyword, value in keywords.items():
            if value is None:
                continue
            try:
                location = location.format(**{keyword: value})
            except KeyError:
                # then this mean scan_dir has not been provided
                pass
        return location


def dump_normalization_array_for_nabu(
    scan: TomwerScanBase, output_file: str, array: Union[numpy.ndarray, float, int]
) -> DataUrl:
    if not isinstance(array, (numpy.ndarray, float, int)):
        raise TypeError(
            f"array is expected to be a numpy array or a scalar and not {type(array)}"
        )
    # save the value to a dedicated path in "nabu_tomwer_serving_hatch"
    if isinstance(scan, HDF5TomoScan):
        entry_path = scan.entry
    elif isinstance(scan, EDFTomoScan):
        entry_path = "entry"
    else:
        raise TypeError
    with HDF5File(output_file, mode="a") as h5f:
        serving_hatch_data_path = None
        # create a unique dataset path to avoid possible conflicts
        while serving_hatch_data_path is None or serving_hatch_data_path in h5f:
            serving_hatch_data_path = "/".join([entry_path, str(uuid.uuid1())])
        # adapt value to what nabues expects.
        if isinstance(array, (float, int)) or (
            isinstance(array, numpy.ndarray) and array.ndim == 1 and len(array) == 1
        ):
            dim_1 = scan.dim_1
            array = numpy.asarray(
                numpy.asarray([array] * len(scan.projections) * dim_1)
            )
            array = array.reshape(len(scan.projections), dim_1)
        elif isinstance(array, numpy.ndarray) and array.ndim == 1:
            dim_1 = scan.dim_1
            array = numpy.repeat(array, dim_1).reshape(len(array), dim_1)

        h5f[serving_hatch_data_path] = array
    file_path = os.path.join(
        settings.NABU_CFG_FILE_FOLDER, settings.NABU_TOMWER_SERVING_HATCH
    )
    return DataUrl(
        file_path=file_path,
        data_path=serving_hatch_data_path,
        scheme="silx",
    )
