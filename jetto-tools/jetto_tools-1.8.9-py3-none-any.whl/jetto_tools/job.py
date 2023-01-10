"""JETTO job management module"""

import os
import re
import subprocess
import shutil
import collections
import tempfile
import uuid
import tarfile
import json
import glob
import numpy as np
from typing import Dict, List, Tuple
from operator import mul
from functools import reduce

import prominence
from prominence.exceptions import ProminenceError

import jetto_tools.config
import jetto_tools._utils as _utils


class JobManagerError(Exception):
    """Generic exception used for all job management errors"""
    pass


class JobManager:
    """Class for managing JETTO jobs"""

    _USERS_HOME_ENV = 'USERS_HOME'
    _RUNS_HOME_ENV = 'RUNS_HOME'

    _JETTO_SOURCE_DIR_REGEX = r"""
        \s*             # Match zero or more whitespace
        JETTO           # Match 'JETTO'
        \s+             # Match at least one space
        GIT             # Match 'GIT'
        \s+             # Match at least one space
        repository      # Match 'repository'
        \s*             # Match any amount of whitespace
        :               # Match ':'
        \s*             # Match any amount of whitespace
        (?P<path>/\S*)  # Match a path - record in group as 'path' 
        \s*             # Match any amount of whitespace        
    """
    _JETTO_SOURCE_DIR_PATTERN = re.compile(_JETTO_SOURCE_DIR_REGEX, re.VERBOSE)

    def submit_job_to_batch(self, config: jetto_tools.config.RunConfig, rundir: str, run=False) -> List:
        """Submit one or more JETTO runs to the batch system

        Exports the configuration, followed by the run scripts (``.llcmd``, ``rjettov``, and ``utils``). Submits the
        job to the batch system, if requested. A ``run`` value of True is equivalent to ``Run Job Now`` in JAMS;
        False is equivalent to ``Set Up Job But Don't Run``.

        Note that this function will only work correctly if called from within the JET batch system environment.
        Calling it from within other environments will fail.

        Returns a list of ``Job``, where each element of the list is a job corresponding to one of the runs defined by
        the configuration

        :param config: Configuration for the run
        :type config: jetto_tools.config.RunConfig
        :param rundir: Relative path to the run directory, with respect to the ``$RUNS_HOME/jetto/runs`` directory
        :type rundir: str
        :param run: If True, create the files and run the job. If False, only create the files.
        :type run: bool
        :return: List of jobs
        :rtype: List[Job]
        :raise: JobManagerError if any aspect of submitting the job fails
        """
        jetto_source_dir = JobManager._find_jetto_source_dir(config)
        runs_home = os.path.join(JobManager._get_run_root(), rundir)

        pointdirs = config.export(runs_home, rundir)
        for pointdir in pointdirs:
            JobManager._export_rjettov_script(jetto_source_dir, pointdir)
            JobManager._export_utils_script(jetto_source_dir, pointdir)
            batchfile_path = JobManager._export_batchfile(config, pointdir)

            if run:
                JobManager._batch_submit(batchfile_path)

        return [Job(pointdir) for pointdir in pointdirs]

    def submit_job_to_prominence(self, config: jetto_tools.config.RunConfig, rundir: str) -> int:
        """Submit a JETTO run to PROMINENCE

        Exports the configuration to the ``rundir``, followed by submitting the job to PROMINENCE. Note that this
        function is designed to be called from within the JET batch system environment. To call it from other
        environments, the ``RUNS_HOME`` environment variable must exist and contain the path to the home directory for
        JETTO runs. The ``$RUNS_HOME`` directory must further contain the path to the run root directory, given by
        ``$RUNS_HOME/jetto/runs``.

        If the configuration contains one or more parameter scans, then the run will be submitted to PROMINENCE as a
        workflow using a job factory, which iterates over each of the working directories corresponding to each point
        in the scan. If the configuration only contains a single point, then it will be submitted to PROMINENCE as
        a regular job, in the same manner as used by JAMS.

        Records the PROMINENCE job/workflow id in a file ``remote.jobid`` in the run directory, in a similar manner to
        JAMS.

        :param config: Configuration for the run
        :type config: jetto_tools.config.RunConfig
        :param rundir: Relative path to the run directory, with respect to the ``$RUNS_HOME/jetto/runs`` directory
        :type rundir: str
        :return: PROMINENCE job/workflow id
        :rtype: int
        :raise: JobManagerError if any aspect of submitting the job fails (including PROMINENCE failures)
        """
        client = prominence.client.ProminenceClient(authenticated=True)

        runpath = os.path.join(JobManager._get_run_root(), rundir)
        pointdirs = config.export(runpath, rundir)

        tarball_path = JobManager._prom_create_tarball(runpath, rundir)
        JobManager._prom_upload_tarball(tarball_path, client)

        if config._npoints() == 1:
            id = JobManager._prom_submit_job(config, runpath, rundir, tarball_path, client)
        else:
            id = JobManager._prom_submit_workflow(config, runpath, rundir, tarball_path, client, pointdirs)

        with open(os.path.join(runpath, 'remote.jobid'), 'wt') as f:
            f.write(f'Job submitted with id {id}\n')

        return id

    @classmethod
    def _find_jetto_source_dir(cls, config: jetto_tools.config.RunConfig) -> str:
        """Find the JETTO source distribution to use

        Based on the configured JETTO version, locates the JETTO source distribution for that version. In line with the
        approach used by JAMS, the JETTO executable is located by combining the ``USERS_HOME`` environment variable
        with the JETTO load module version set in the suppleid configuration. The JETTO executable is run in verbose
        mode (i.e. with the ``-v`` switch). The information returned by JETTO is parsed to locate the source
        distribution.

        :param config: Run configuration
        :type config: jetto_tools.config.RunConfig
        :return: Path to the source distribution
        :rtype: str
        :raise: JobManagerError if the path cannot be determined from the supplied configuration
        """
        load_module_path = cls._find_load_module_path(config)

        if not os.path.isfile(load_module_path):
            raise JobManagerError(f'JETTO executable at {load_module_path} not found')

        completed_process = subprocess.run([f'{load_module_path}', '-v'], encoding='utf-8', capture_output=True)
        if completed_process.returncode != 0:
            raise JobManagerError(f'Call to "{load_module_path} -v" failed')

        match = cls._JETTO_SOURCE_DIR_PATTERN.match(completed_process.stdout)
        if not match:
            raise JobManagerError(f'Unable to parse JETTO executable output "{completed_process.stdout}"')

        return match.group('path')

    @classmethod
    def _find_load_module_path(cls, config):
        """Determine the path to the JETTO load module

        Constructs the load module path as ``$USERS_HOME/<config.userid>/jetto/bin/linux/<config.binary>[_mpi]_64``,
        where the ``_mpi`` string is omitted if the run is serial

        :param config: Run configuration
        :type config: jetto_tools.config.RunConfig
        :return: The path to the load module
        :rtype: str
        :raise: JobManagerError if the ``USERS_HOME`` environment variable does not exist
        """
        if cls._USERS_HOME_ENV not in os.environ:
            raise JobManagerError(f'Environment variable {cls._USERS_HOME_ENV} not found')
        home = os.environ[cls._USERS_HOME_ENV]

        load_module_path = os.path.join(home, config.userid, 'jetto/bin/linux', config.binary)

        if config.processors > 1:
            load_module_path = load_module_path + '_mpi_64'
        else:
            load_module_path = load_module_path + '_64'

        return load_module_path

    @classmethod
    def _export_rjettov_script(cls, jetto_source_dir: str, rundir: str):
        """Export the ``rjettov`` script

        Copies the ``rjettov`` script from the JETTO source tree into the run directory

        :param jetto_source_dir: Path to the top of the JETTO source distribution in use
        :type jetto_source_dir: str
        :param rundir: JETTO run directory to export the script to
        :type rundir: str
        """
        jetto_rjettov_script_src_path = os.path.join(jetto_source_dir, 'sh/rjettov')
        if not os.path.isfile(jetto_rjettov_script_src_path):
            raise JobManagerError(f'JETTO rjettov script at {jetto_rjettov_script_src_path} not found')

        jetto_rjettov_script_dest_path = os.path.join(rundir, 'rjettov')
        shutil.copy(jetto_rjettov_script_src_path, jetto_rjettov_script_dest_path)

    @classmethod
    def _export_utils_script(cls, jetto_source_dir: str, rundir: str):
        """Export the ``utils`` script

        Copies the ``utils`` script from the JETTO source tree into the run directory. If the utils script does
        not exist, this function has no effect (this is required for backwards compatibility with older versions of
        JETTO, where the utils script did not exist).

        :param jetto_source_dir: Path to the top of the JETTO source distribution in use
        :type jetto_source_dir: str
        :param rundir: JETTO run directory to export the script to
        :type rundir: str
        """
        jetto_utils_script_src_path = os.path.join(jetto_source_dir, 'sh/utils')
        if os.path.isfile(jetto_utils_script_src_path):
            jetto_utils_script_dest_path = os.path.join(rundir, 'utils')
            shutil.copy(jetto_utils_script_src_path, jetto_utils_script_dest_path)

    @classmethod
    def _export_batchfile(cls, config: jetto_tools.config.RunConfig, pointdir: str) -> str:
        """Export the run batchfile

        Generates a new batchfile (``.llcmd``) in the run directory. The batchfile is configured according to the
        export directory path, the number of processors and the JETTO version.

        :param config: Run configuration
        :type config: jetto_tools.config.RunConfig
        :param pointdir: Path to the point export directory
        :type pointdir: str
        :return: The path to the exported batchfile
        :rtype: str
        """
        run_root = cls._get_run_root()

        batchfile = _Batchfile(run_root=run_root,
                               rel_path=os.path.relpath(pointdir, run_root),
                               processors=config.processors,
                               binary=config.binary,
                               userid=config.userid)

        batchfile_path = os.path.join(pointdir, '.llcmd')
        with open(batchfile_path, 'w') as f:
            f.write(str(batchfile))

        return batchfile_path

    @classmethod
    def _batch_submit(cls, batchfile_path: str):
        """Call the batch submission command

        Switches the working directory to ``$RUNS_HOME``, and calls the ``llsubmit`` commmand to submit the job
        described by the supplied batchfile

        :param batchfile_path: Path to the batchfile for the job
        :type batchfile_path: str
        :raise: JobManagerError if the ``RUNS_HOME`` environment variable does not exist, or if the call to the
                ``llsubmit`` command fails
        """
        runs_home = cls._get_runs_home()
        batch_submitter = cls._find_batch_submit_cmd()
        
        debug_file_path = f'{batchfile_path}.dbg'
        with open(debug_file_path, 'w') as debug_file:
            cmd = [f'{batch_submitter}', f'{batchfile_path}']
            completed_process = subprocess.run(cmd, cwd=runs_home, encoding='utf-8',
                                               stdout=debug_file, stderr=debug_file)
            if completed_process.returncode != 0:
                raise JobManagerError(f'Call to llsubmit failed for batchfile {batchfile_path} '
                                      f'(args: "{completed_process.args}" return code: {completed_process.returncode}, '
                                      f'see "{(debug_file_path)}" for captured output')

    @classmethod
    def _get_runs_home(cls):
        """Get RUNS_HOME

        Returns the value of the RUNS_HOME environment variable

        :return: The value of $RUNS_HOME
        :rtype: str
        :raise: JobManagerError if the environment variable doesn't exist
        """
        if cls._RUNS_HOME_ENV not in os.environ:
            raise JobManagerError(f'Environment variable {cls._RUNS_HOME_ENV} not found')

        return os.environ[cls._RUNS_HOME_ENV]

    @classmethod
    def _get_run_root(cls):
        """Get the path to the JETTO run root directory

        The run root directory is given by $RUNS_HOME/jetto/runs

        :return: Run root path
        :rtype: str
        :raise: JobManagerError if the environment variable $RUNS_HOME doesn't exist
        """
        return os.path.join(cls._get_runs_home(), 'jetto/runs')

    @classmethod
    def _find_batch_submit_cmd(cls):
        """Determine the batch submission command

        Uses the environment's ``batch_submit`` script to determine the appropriate batch submission command

        :return: The batch submission command
        :rtype: str
        :raise: JobManagerError if the call to ``batch_submit`` fails
        """
        completed_process = subprocess.run(['batch_submit'], encoding='utf-8', capture_output=True)
        if completed_process.returncode != 0:
            raise JobManagerError(f'Call to batch_submit failed '
                                  f'(return code {completed_process.returncode})')

        return completed_process.stdout.strip()

    @classmethod
    def _prom_create_tarball(cls, runpath: str, rundir: str) -> str:
        """Create a tarball out of the run directory contents

        Creates the tarball under /tmp. File name is <rundir>-<uuid>.tgz, where rundir has any forward slash
        replaced with '-'. The tarball contains the contents of the run directory, without any prefix (e.g. if the run
        directory was set to ``foo/bar``, then the tarball root contains the contents of the ``bar`` directory.
        Returns the full path to the created tarball.

        When adding files to the tarball, the JSET files (``jetto.jset``) are excluded, as they aren't used by JETTO
        at runtime, and they would add significantly to the size of the generated tarball.

        :param runpath: Full path to the run directory
        :type runpath: str
        :param rundir: Path to the run directory, relative to the run root
        :type rundir: str
        :return: Path to the tarball
        :rtype: str
        """
        def _filter(tarinfo):
            if tarinfo.name.endswith('jetto.jset'):
                return None
            else:
                return tarinfo

        tarball_name = f'{cls._prom_name(rundir)}-{uuid.uuid4()}.tgz'
        tarball_path = os.path.join('/tmp', tarball_name)

        with tarfile.open(tarball_path, "w:gz") as tar_handle:
            tar_handle.add(runpath, arcname=os.path.basename(rundir), filter=_filter)

        return tarball_path

    @classmethod
    def _prom_upload_tarball(cls, path: str, client: prominence.client.ProminenceClient):
        """Upload a tarball to PROMINENCE

        Uses the PROMINENCE client to upload  the tarball at *path* to PROMINENCE. The file name in the upload is simply
        the tarball file name, without any path prefix.

        :param path: Full path to the tarball
        :type path: str
        :param client: PROMINENCE client
        :type client: prominence.client.ProminenceClient
        :raise: JobManagerError if the upload fails
        """
        try:
            client.upload(os.path.basename(path), path)
        except ProminenceError as err:
            raise JobManagerError(str(err))

    @classmethod
    def _prom_task_description(cls, config: jetto_tools.config.RunConfig, factory=False) -> List[Dict]:
        """Create the PROMINENCE task description

        Populates and returns the content of the 'task' field in a PROMINENCE job description. The work directory in the
        JETTO run command is either set to ``prom`` for a normal job, or is parametrised to ``$workdir`` if we are
        submitting a parameter scan using a job factory.

        :param config: Run configuration
        :type config: jetto_tools.config.RunConfig
        :param factory: Create a command where the work directory is parameterised
        :type factory: bool
        :return: Task description
        :rtype: List containing single task description dict
        """
        if factory:
            workdir = '$workdir'
        else:
            workdir = 'prom'

        if config.processors > 1:
            cmd = f'rjettov -xmpi -x64 -S {workdir} build docker'
        else:
            cmd = f'rjettov -x64 -S {workdir} build docker'

        return [{
            'cmd': cmd,
            'image': f'CCFE/JINTRAC/{config.userid}:{config.binary}.tgz',
            'runtime': 'udocker'
        }]

    @classmethod
    def _prom_resource_description(cls, config: jetto_tools.config.RunConfig) -> Dict:
        """Create the PROMINENCE resource description

        Populates and returns the content of the 'resources' field in a PROMINENCE job description.

        :param config: Run configuration
        :type config: jetto_tools.config.RunConfig
        :return: Resource description
        :rtype: Dict
        :raise: JobManagerError if the configured walltime is not numeric
        """
        if not _utils.is_numeric(config.walltime):
            raise JobManagerError(f'Invalid value {config.walltime} for configured walltime')

        return {
            'cpus': config.processors,
            'memory': max(2 * config.processors, 6),
            'disk': 10,
            'nodes': 1,
            'walltime': int(config.walltime * 60)
        }

    @classmethod
    def _prom_submit_job(cls, config: jetto_tools.config.RunConfig, runpath: str, rundir: str,
                         tarball_path: str, client: prominence.client.ProminenceClient):
        """Create and submit a PROMINENCE job

        Constructs a job description based on the supplied configuration, and submits it via the PROMINENCE API.

        :param config: Run configuration
        :type config: jetto_tools.config.RunConfig
        :runpath: Full path to the run directory
        :type runpath: str
        :param rundir: Relative path to the run directory, from the run root
        :type rundir: str
        :tarball_path: Full path to the job tarball
        :type tarball_path: str
        :client: PROMINENCE client
        :type client: prominence.client.ProminenceClient
        :return: PROMINENCE job id
        :rtype: int
        :raise: JobManagerError if the submission fails
        """
        job_ = cls._prom_job_description(config, rundir, runpath, tarball_path)

        try:
            id = client.create_job(job_)
        except ProminenceError as err:
            raise JobManagerError(str(err))

        return id

    @classmethod
    def _prom_submit_workflow(cls, config: jetto_tools.config.RunConfig, runpath: str, rundir: str,
                              tarball_path: str, client: prominence.client.ProminenceClient,
                              pointdirs: List[str]) -> int:
        """Create and submit a PROMINENCE workflow

        Constructs a workflow description based on the supplied configuration, and submits it via the PROMINENCE API.

        :param config: Run configuration
        :type config: jetto_tools.config.RunConfig
        :runpath: Full path to the run directory
        :type runpath: str
        :param rundir: Relative path to the run directory, from the run root
        :type rundir: str
        :param tarball_path: Full path to the job tarball
        :type tarball_path: str
        :param client: PROMINENCE client
        :type client: prominence.client.ProminenceClient
        :param pointdirs: List of point directory paths, relative to the run root
        :type pointdirs: List of strings
        :return: PROMINENCE workflow id
        :rtype: int
        :raise: JobManagerError if the submission fails
        """
        workflow = {
            'name': cls._prom_name(rundir),
            'jobs': [cls._prom_job_description(config, rundir, runpath, tarball_path, workflow=True)],
            'factories': [
                {
                    'name': cls._prom_name(rundir),
                    'jobs': [cls._prom_name(rundir)],
                    'type': 'zip',
                    'parameters': [
                        {
                            'name': 'workdir',
                            'values': [f'prom/{os.path.basename(path)}' for path in pointdirs]
                        }
                    ]
                }
            ]
        }

        try:
            id = client.create_workflow(workflow)
        except ProminenceError as err:
            raise JobManagerError(str(err))

        return id

    @classmethod
    def _prom_name(cls, rundir: str) -> str:
        """Generate a PROMINENCE job/workflow name

        Generates the name by replacing directory separators (forward slashes) with
        hyphens.

        :param rundir: Path to run directory, relative to run root
        :type rundir: str
        :return: Name
        :rtype: str
        """
        return rundir.replace('/', '-')

    @classmethod
    def _prom_job_description(cls, config: jetto_tools.config.RunConfig, rundir: str, runpath: str,
                              tarball_path: str, workflow=False) -> Dict:
        """Generate a PROMINENCE job description

        Construct the PROMINENCE job dictionary describing each aspect of the submitted job

        :param config: Run configuration
        :type config: jetto_tools.config.RunConfig
        :runpath: Full path to the run directory
        :type runpath: str
        :param rundir: Relative path to the run directory, from the run root
        :type rundir: str
        :tarball_path: Full path to the job tarball
        :type tarball_path: str
        :param workflow: Flag indicating if the job is part of a workflow
        :type workflow: bool
        :return: Job description
        :rtype: Dict
        """
        return {
            'name': cls._prom_name(rundir),
            'tasks': cls._prom_task_description(config, factory=workflow),
            'resources': cls._prom_resource_description(config),
            'artifacts': [
                {
                    'url': os.path.basename(tarball_path),
                    'mountpoint': f'{os.path.basename(rundir)}:/jetto/runs/prom'
                }
            ],
            'labels': {
                'app': 'jintrac',
                'fullpath': runpath,
                'codeid': 'jetto'
            },
            'outputDirs': [
                os.path.basename(rundir)
            ],
            'notifications': [
                {
                    'event': 'jobFinished', 'type': 'email'
                }
            ],
            'policies': {
                'maximumTimeInQueue': 7 * 24 * 60,
                'leaveInQueue': True,
                'autoScalingType': None
            }
        }


_BatchfileNamedTuple = collections.namedtuple('_BatchfileNamedTuple',
                                              ['processors', 'run_root', 'rel_path', 'binary', 'userid'])
_BatchfileNamedTuple.__new__.__defaults__ = (1, '', '', '', '')


class _Batchfile(_BatchfileNamedTuple):
    """Helper class for generation of the contents of a batchfile"""
    def __str__(self):
        """Write the contents of the batchfile to a string"""
        if self.processors > 1:
            processor_dependent_string = (f'# @ jobtype = openmpi\n'
                                          f'# @ min_processors = {self.processors}\n'
                                          f'# @ max_processors = {self.processors}\n')
            mpi_string = ' -xmpi'
        else:
            processor_dependent_string = ''
            mpi_string = ''

        rel_path_dots = self.rel_path.replace('/', '.')
        pointdir = os.path.join(self.run_root, self.rel_path)

        return ('#!/bin/sh\n'
                f'# @ job_name = jetto.{rel_path_dots}\n'
                '# @ input = /dev/null\n'
                '# @ output = ll.out\n'
                '# @ error = ll.err\n'
                '# @ restart = no\n'
                '# @ checkpoint = no\n'
                '# @ environment = COPY_ALL\n'
                f'{processor_dependent_string}'
                '\n'
                f'# @ initialdir = {pointdir}\n'
                f'# @ executable = {pointdir}/rjettov\n'
                f'# @ arguments = -S -p{mpi_string} -x64 {self.rel_path} {self.binary} {self.userid}\n'
                '# @ queue\n'
                '\n')


class Status:
    """Status of a JETTO job"""
    SUCCESSFUL = 0
    FAILED = 1
    UNKNOWN = 2

    @classmethod
    def to_string(cls, status):
        return {
            cls.SUCCESSFUL: "Successful",
            cls.FAILED: "Failed",
            cls.UNKNOWN: "Unknown"
        }[status]


class JobError(Exception):
    """Generic exception used for all job errors"""
    pass


class Job:
    """Class representing a single JETTO job

    This class allows the user to query the running status of a job, and also to retrieve characteristics of the job
    such as the run directory and the job ID
    """

    def __init__(self, rundir: str):
        """Initialise a job

        Initialise a job based on the contents of the job's run directory. The files in the run directory are used to
        determine the job's configuration and current status. The presence or absence of the ``.llcmd.dbg`` file
        indicates whether or not the job has been run. The ``serialisation.json`` file is used to extract the job's
        configuration.

        :param rundir: Path to the job's run directory
        :type rundir: str
        :raise: JobError if the job's serialisation cannot be retrieved
        """
        if not os.path.isdir(rundir):
            raise JobError(f'Run directory {rundir} not found')

        self._rundir = rundir

        llcmd_dbg = os.path.join(rundir, '.llcmd.dbg')
        if not os.path.isfile(llcmd_dbg):
            self._id = None
        else:
            self._id = Job._parse_llcmd_dbg(llcmd_dbg)

        serialisation = os.path.join(rundir, 'serialisation.json')
        if not os.path.isfile(serialisation):
            self._serialisation = None
        else:
            with open(serialisation) as f:
                try:
                    self._serialisation = json.load(f)
                except json.decoder.JSONDecodeError as err:
                    raise JobError(f'File {serialisation} cannot be parsed ({str(err)})')

    def __repr__(self):
        """Get's the job's representation

        Returns a string in the format ``Job(<rundir>)``
        """
        return f"{self.__class__}({self._rundir})"

    def __str__(self):
        """Get's the job's printable string representation

        Returns a string in the format ``JETTO job (ID: <job id>, Run directory: <run directory>, Status: <status>)``
        """
        return f"JETTO job (ID: {self._id}, Run directory: {self._rundir}, Status: {Status.to_string(self.status())})"

    @property
    def rundir(self):
        """Get the path of the job's run directory

        Returns the path supplied when the job was created

        :return: Path to the run directory
        :rtype: str
        """
        return self._rundir

    @property
    def id(self):
        """Get the ID of the job

        The ID is the one returned by LoadLeveller when the job is submitted (normally found in the .lldbg file
        created by JAMS). If the job was not submitted, the ID is None

        :return: ID of the job
        :rtype: integer (or None if the job hasn't been submitted)
        """
        return self._id

    @property
    def serialisation(self) -> Dict:
        """Get the job's serialisation

        Returns the serialisation generated when the job was submitted. The serialisation is a dictionary describing
        the configuration of the job

        :return: The job's serialisation
        :rtype: Dict
        """
        return self._serialisation

    _LLCMD_DBG_REGEX = r"""
         (?P<id> \d+ )          # Match ID surrounded by spaces - record as "id"
         """
    _LLCMD_DBG_PATTERN = re.compile(_LLCMD_DBG_REGEX, re.VERBOSE)

    def status(self) -> int:
        """Get the current status of the JETTO job

        Status is determined by looking at the ``jetto.out`` log file and parsing the last lines of the file. Depending
        on whether or not the string 'Terminating successfully' is found in the last lines of the file, the status is
        determined.

        Status can be one of:

         * Status.SUCCESSFUL: The job has completed successfully (the string has been found)
         * Status.FAILED: The job has completed with a failure (the string has not been found)
         * Status.UNKNOWN: The job's status cannot be determined (the ``jetto.out`` file does not exist)

         :return: Status of the job
         :rtype: int
        """
        outfile = os.path.join(self._rundir, 'jetto.out')
        if not os.path.isfile(outfile):
            return Status.UNKNOWN

        with open(outfile) as f:
            outfile_contents = collections.deque(f, 30)

        if any('Terminating successfully' in line for line in outfile_contents):
            status = Status.SUCCESSFUL
        else:
            status = Status.FAILED

        return status

    @classmethod
    def _parse_llcmd_dbg(cls, llcmd_dbg: str) -> int:
        """Parse the contents of a ``.llcmd.dbg`` file

        Extracts the job identifier from the file

        :return: Job ID
        :rtype: None
        :raise: JobError if the file cannot be parsed
        """
        with open(llcmd_dbg, 'r') as f:
            s = f.read()

        matches = cls._LLCMD_DBG_PATTERN.search(s)
        if matches is None:
            raise JobError(f'Unable to parse file {llcmd_dbg}')

        return int(matches.group('id'))


def retrieve_jobs(run_root: str) -> List[Job]:
    """Retrieve jobs from the run root of a scan

    Given the run root of a scan, creates a job associated with each point in the scan. Returns the list of jobs
    created.

    :param run_root: Path to the root run directory of the scan
    :type run_root: str
    :return: List of scan jobs
    :rtype: List[Job]
    :raise: JobError if there are no point directories in the scan, or if any of the directories cannot be turned into
    a Job
    """
    pathname = os.path.join(run_root, 'point_*')
    pointdirs = sorted(glob.glob(pathname))

    if not pointdirs:
        raise JobError(f'No point directories found in {run_root}')

    return [Job(p) for p in pointdirs]


def prominence_download_scan_results(workflow_id: int, outdir: str, verbose: bool = False, points=None):
    """Download scan results from PROMINENCE

    Downloads the results of the PROMINENCE jobs corresponding to the given ``workflow_id``. Each point directory
    containing results files is downloaded separately and placed in ``outdir``.

    The user can optionally filter on which points within a scan they want to download. This can be useful for
    retrieving specific points or ranges of points which had not completed previosuly.

    :param workflow_id: Id of the PROMINENCE workflow running the scan
    :type workflow_id: int
    :param outdir: Directory in which to place the downloaded point directories
    :type outdir: str
    :param verbose: Print out a running log of downloads
    :type verbose: bool
    :param points: List of point numbers to download from the scan. If None, all points are downloaded.
    :type points: List[int]
    """
    def _pointdir_from_job(job):
        return os.path.basename(job['parameters']['workdir'])

    def _point_from_job(job):
        return int(_pointdir_from_job(job).split('_')[-1])

    client = prominence.ProminenceClient(authenticated=True)

    jobs = client.list_jobs(status='all', workflow_id=workflow_id)

    outdir = os.path.abspath(outdir)
    cwd = os.getcwd()

    jobs = sorted(jobs, key=_pointdir_from_job)
    if points is not None:
        jobs = [job for job in jobs if _point_from_job(job) in points]

    for job in jobs:
        os.chdir(cwd)

        point_dir = _pointdir_from_job(job)
        point = _point_from_job(job)

        root = job['name'].split('/')[0]

        if verbose:
            print(f'Downloading {point_dir}...')

        if job['status'] != 'completed':
            if verbose:
                print(f'Skipping {point_dir} - not completed')
            continue

        with tempfile.TemporaryDirectory() as tempdir:
            proc = subprocess.run(['prominence',  'download',  f'{job["id"]}'], cwd=tempdir, capture_output=True)
            if proc.returncode != 0:
                if verbose:
                    print(f'Download of {point_dir} - failed')

            os.chdir(tempdir)
            tarfile_name = f"{root}.tgz"
            with tarfile.open(tarfile_name) as tarball:
                members = [tarinfo for tarinfo in tarball.getmembers()
                           if tarinfo.name.startswith(f'{root}/{point_dir}')]
                tarball.extractall(members=members)

                # Using the shell cp command rather than shutil.copytree, as the latter cannot overwrite for Python
                # versions < 3.8
                subprocess.run(['cp', '-rf', os.path.join(root, point_dir), os.path.join(outdir, point_dir)])

                tarball_serialisation = os.path.join(root, 'serialisation.json')
                dst_serialisation = os.path.join(outdir, 'serialisation.json')
                if not os.path.isfile(dst_serialisation):
                    serialisation_member = tarball.getmember(tarball_serialisation)
                    tarball.extract(serialisation_member)
                    shutil.copyfile(tarball_serialisation, dst_serialisation)
