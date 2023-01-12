from pathlib import Path
import shutil
import tempfile
from typing import Optional
import os
from tomwer.slurm.utils import SubProcessCommand
from .utils import has_scancel_available, has_scontrol_available
import time
import logging

_logger = logging.getLogger(__name__)


class Job:
    def __init__(self, working_directory) -> None:
        """
        :param script: script to be launched
        """
        self._working_directory = working_directory
        self._dry_run = False
        self._result = "not run yet"

    @property
    def working_directory(self) -> Optional[str]:
        return self._working_directory

    @property
    def result(self):
        return self._result

    @property
    def dry_run(self):
        return self._dry_run

    @dry_run.setter
    def dry_run(self, dry_run: bool):
        self._dry_run = dry_run

    def run(self):
        raise NotImplementedError("Base class")


class ScriptJob(Job):
    def __init__(
        self,
        script: tuple,
        working_directory: Optional[Path] = None,
        script_path: Optional[Path] = None,
        clean_script: bool = True,
        clean_job_artefacts: bool = True,
    ) -> None:
        """
        :param tuple script: script with a tuple of str (one per line to write)
        """
        if not isinstance(script, tuple):
            raise TypeError(
                f"script is expected to be a tuple. {type(script)} provided"
            )
        super().__init__(working_directory)
        self._clean_script = clean_script
        self._script_path = script_path
        self._script = list(script)
        self._overwrite = False
        self._file_extension = "sh"
        self._clean_job_artefacts = clean_job_artefacts

    @property
    def script(self) -> tuple:
        return tuple(self._script)

    @property
    def file_extension(self):
        return self._file_extension

    @file_extension.setter
    def file_extension(self, file_extension: str):
        self._file_extension = file_extension.lsplit(".")

    @property
    def overwrite(self) -> bool:
        return self._overwrite

    @overwrite.setter
    def overwrite(self, overwrite: bool):
        self._overwrite = overwrite

    @property
    def script_path(self) -> Optional[Path]:
        return self._script_path

    @property
    def clean_script(self):
        return self._clean_script

    @clean_script.setter
    def clean_script(self, clean_script: bool):
        self._clean_script = clean_script

    @property
    def clean_job_artefacts(self) -> bool:
        return self._clean_job_artefacts

    @clean_job_artefacts.setter
    def clean_job_artefacts(self, clean: bool):
        return self._clean_job_artefacts

    def _save_script(self) -> Path:
        if self.script_path is not None:
            if os.path.exists(self.script_path) and not os.path.isfile(
                self.script_path
            ):
                raise ValueError(
                    f"script_path is expected to be a file path ({self.script_path})"
                )
        else:
            self._script_path = ".".join(
                [tempfile.NamedTemporaryFile().name, self.file_extension]
            )
        os.makedirs(os.path.dirname(self.script_path), exist_ok=True)
        # warning: for compatiblity with batchScript the file should always be set to self._script_path
        # before calling _write_script_preprocessing_lines
        mode = "w" if self.overwrite else "x"
        with open(self.script_path, mode=mode) as file_object:
            self._specify_shell_command(file_object)
            self._write_script_preprocessing_lines(file_object)
            self._write_script_lines(file_object)
            self._write_script_postprocessing_lines(file_object)
        return self.script_path

    def _specify_shell_command(self, file_object):
        file_object.write("#!/bin/bash\n")

    def _write_script_lines(self, file_object):
        for line in self.script:
            file_object.write(line + "\n")

    def _write_script_preprocessing_lines(self, file_object):
        if self._working_directory is not None:
            file_object.write(f"#SBATCH --chdir={self.working_directory}\n")

    def _write_script_postprocessing_lines(self, file_object):
        pass

    def _do_script_cleaning(self):
        if self.script_path is not None and os.path.isfile(self.script_path):
            os.remove(self.script_path)

    def _do_job_artefacts_cleaning(self):
        pass


class SBatchScriptJob(ScriptJob):
    def __init__(self, slurm_config: Optional[dict] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        assert isinstance(slurm_config, (dict, type(None)))
        self._job_id = None
        self._status = "Under submission"
        self._slurm_config = slurm_config if slurm_config is not None else {}

        self._pycuda_cache_dir = os.path.join(
            os.path.dirname(self.script_path), ".pycuda_cache_dir"
        )
        # as we can have some incoherent home directory we need for some computer to define the pycuda cache directory (for iccbm181 for example)
        self._script.insert(0, f"mkdir -p {self._pycuda_cache_dir}")
        self._script.insert(1, f"export PYCUDA_CACHE_DIR={self._pycuda_cache_dir}")

    def set_status(self, status):
        self._status = status

    @property
    def job_id(self):
        return self._job_id

    @job_id.setter
    def job_id(self, job_id: int):
        self._job_id = job_id

    @property
    def status(self):
        return self._status

    def get_status(self):
        return self._status

    def run(self):
        self._status = "Running"
        script_path = self._save_script()
        if not os.path.exists(script_path):
            raise OSError(
                f"{script_path} doesn't exists. Unable to write script file. Can be write rights error."
            )
        if self.dry_run is False:
            job_id = SubProcessCommand(command=f"sbatch {script_path}").run()
        else:
            job_id = "-1"
        self._result = self._get_job_id_or_raise_error(job_id)
        if self.clean_script:
            self._do_script_cleaning()
        if self.clean_job_artefacts:
            self._do_job_artefacts_cleaning()
        return self._result

    def _get_job_id_or_raise_error(self, text: str) -> int:
        try:
            # we expect the slurm job ID to be the last element of the string
            return int(text.replace("\n", "").split(" ")[-1])
        except Exception as e:
            raise ValueError("Fail to get job id from submission") from e

    def _specify_shell_command(self, file_object):
        file_object.write("#!/bin/bash\n")

    def _write_script_preprocessing_lines(self, file_object):
        super()._write_script_preprocessing_lines(file_object=file_object)
        # handle first
        slurm_lines, pre_processing_lines = self.interpret_slurm_config(
            self._slurm_config
        )
        # define out file
        output_file_path = (
            str(self.script_path)[: -(len(self.file_extension) + 1)] + ".out"
        )
        file_object.write(f"#SBATCH --output={output_file_path}\n")

        for slurm_line in slurm_lines:
            file_object.write(slurm_line + "\n")
        for pre_processing_line in pre_processing_lines:
            file_object.write(pre_processing_line + "\n")

    def _do_job_artefacts_cleaning(self):
        if os.path.exists(self._pycuda_cache_dir):
            shutil.rmtree(self._pycuda_cache_dir, ignore_errors=True)

    @staticmethod
    def interpret_slurm_config(slurm_config: dict) -> tuple:
        """
        convert a slurm configuration dictory to a tuple of two tuples.
        The first tuple will provide the lines to add to the shell script for sbtach (ressources specification)
        The second line will provide some command to run before the 'processing command' like sourcing a python virtual environment

        :param dict slurm_config: slurm configuration to be interpreted
        :raise: KeyError if one the `slurm_config` dict cannot be interpreted
        """
        if not isinstance(slurm_config, dict):
            raise TypeError(
                f"slurm_config is expected to be a dict. {type(slurm_config)} provided"
            )
        slurm_ressources = []
        preprocessing = []
        for key, value in slurm_config.items():
            if value is None:
                continue
            if key == "cpu-per-task":
                slurm_ressources.append(f"#SBATCH --cpus-per-task={value}")
            elif key == "n_tasks":
                slurm_ressources.append(f"#SBATCH --ntasks={value}")
            elif key == "memory":
                slurm_ressources.append(f"#SBATCH --mem={value}GB")
            elif key == "partition":
                slurm_ressources.append(f"#SBATCH -p {value}")
            elif key == "n_gpus":
                slurm_ressources.append(f"#SBATCH --gres=gpu:{value}")
            elif key == "job_name":
                slurm_ressources.append(f"#SBATCH -J '{value}'")
            elif key == "walltime":
                slurm_ressources.append(f"#SBATCH -t {value}")
            elif key == "python_venv":
                preprocessing.append(f"source {value}")
            else:
                raise KeyError(f"Unknow slurm configuration key: {key}")
        return tuple(slurm_ressources), tuple(preprocessing)


def get_job_status(job_id):
    if job_id is None:
        return "error"
    elif not has_scontrol_available():
        raise RuntimeError("squeue not available")
    else:
        res = SControlShowJobCommand(job_id=job_id).run()
        job_state = res.get("JobState", "FAILED")
        if job_state.lower() in (
            "out_of_memory",
            "suspended",
            "timeout",
            "nodefail",
            "preempted",
            "boot_fail",
            "deadline",
            " resv_del_hold",
            "revoked",
        ):
            _logger.warning(f"slurm job {job_id} failed with state {job_state}")
            job_state = "FAILED"
        return job_state.lower()


def get_job_infos(job_id):
    if not has_scontrol_available():
        raise RuntimeError("squeue not available")
    else:
        return SControlShowJobCommand(job_id=job_id).run()


def submit_sbatch_job(job):
    job_id = job.run()
    if not type(job_id) == int:
        return
    job.job_id = job_id
    while True:
        job_status = get_job_status(job_id)
        job.set_status(job_status)
        if job_status.lower() in ("completed", "failed", "cancelled", "finished"):
            infos = get_job_infos(job_id)
            job.infos = infos
            return job_status.lower()
        else:
            time.sleep(1)


def cancel_slurm_job(job_id):
    if not has_scancel_available():
        raise RuntimeError("slurm command 'scancel' not available from this computer")
    else:
        return SubProcessCommand(command=f"scancel {job_id}").run()


class SControlShowJobCommand(SubProcessCommand):
    def __init__(self, job_id, platform="Linux"):
        super().__init__(f"scontrol show job {job_id}", platform)

    def interpret_result(self, stdout, stderr):
        return self.stdout_to_dict(stdout=stdout)

    @staticmethod
    def stdout_to_dict(stdout):
        res = {}
        res_splitted = " ".join(stdout.split("\n"))
        res_splitted = res_splitted.split(" ")
        for elements in res_splitted:
            if elements == "":
                continue
            elements_splitted = elements.split("=", maxsplit=1)
            if len(elements_splitted) < 2:
                continue

            key, value = elements_splitted[0], elements_splitted[1]
            res[key] = value
        return res
