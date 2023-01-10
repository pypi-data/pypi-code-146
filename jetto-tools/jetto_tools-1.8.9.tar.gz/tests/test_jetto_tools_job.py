import json

import numpy as np
import pytest
import unittest.mock as mock
import os.path
import stat
import re
import tarfile
import filecmp
import random
import prominence
from prominence.exceptions import ConnectionError, AuthenticationError, FileUploadError, WorkflowCreationError

import jetto_tools.job as job
import jetto_tools.config


@pytest.fixture()
def manager():
    """Pre-built job manager"""
    return job.JobManager()


@pytest.fixture()
def jetto_source_dir(tmpdir):
    dir = tmpdir.mkdir('source')

    return dir


@pytest.fixture()
def jetto_scripts_dir(jetto_source_dir):
    dir = jetto_source_dir.mkdir('sh')

    return dir


@pytest.fixture()
def jetto_run_script(jetto_scripts_dir):
    script_path = jetto_scripts_dir.join('rjettov')
    script_path.write('foo')
    mode = script_path.stat().mode
    script_path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    return script_path


@pytest.fixture()
def jetto_utils_script(jetto_scripts_dir):
    script_path = jetto_scripts_dir.join('utils')
    script_path.write('bar')
    mode = script_path.stat().mode
    script_path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    return script_path


@pytest.fixture()
def jetto_sources(jetto_run_script, jetto_utils_script):
    return jetto_run_script, jetto_utils_script


@pytest.fixture()
def users_home(tmpdir):
    dir = tmpdir.mkdir('home')

    return dir


@pytest.fixture()
def runs_home(tmpdir):
    dir = tmpdir.mkdir('common').mkdir('cmg').mkdir('user')

    return dir


@pytest.fixture()
def run_root(runs_home):
    dir = runs_home.mkdir('jetto').mkdir('runs')

    return dir


@pytest.fixture()
def rundir(run_root):
    run_root.mkdir('runtestdata')

    return 'runtestdata'


@pytest.fixture()
def tar_extract_dir(tmpdir):
    return tmpdir.mkdir('extract')


@pytest.fixture()
def mock_files(run_root):
    """Create three dummy files in the run directory"""
    def _fixture(_self, run_dir):
        run_path = os.path.join(run_root.strpath, run_dir)
        if not os.path.isdir(run_path):
            os.makedirs(run_path, exist_ok=True)

        for file in ('jetto.jset', 'jetto.in', 'serialisation.json'):
            with open(os.path.join(run_root.strpath, run_dir, file), 'wt') as f:
                f.write(file)

        return mock.DEFAULT

    return _fixture


@pytest.fixture()
def mock_config(run_root, rundir, mock_files):
    """Pre-built config in which userid = 'sim' and binary = 'v060619'"""
    m = mock.MagicMock(spec=jetto_tools.config.RunConfig)
    m.userid = 'sim'
    m.binary = 'v060619'
    m.processors = 2
    m.walltime = 2
    m.export.side_effect = mock_files
    m.export.return_value = [os.path.join(run_root.strpath, rundir)]
    m._npoints.return_value = 1

    return m


@pytest.fixture()
def jetto_exe(users_home):
    jetto_exe_dir = users_home.mkdir('sim').mkdir('jetto').mkdir('bin').mkdir('linux')
    jetto_exe_path = jetto_exe_dir.join('v060619_mpi_64')
    jetto_exe_path.write('')

    return jetto_exe_path


@pytest.fixture()
def jetto_exe_serial(users_home):
    jetto_exe_dir = users_home.mkdir('sim').mkdir('jetto').mkdir('bin').mkdir('linux')
    jetto_exe_path = jetto_exe_dir.join('v060619_64')
    jetto_exe_path.write('')

    return jetto_exe_path


@pytest.fixture()
def jintrac_env(monkeypatch, users_home, runs_home, jetto_exe):
    monkeypatch.setenv('USERS_HOME', users_home.strpath)
    monkeypatch.setenv('RUNS_HOME', runs_home.strpath)

    return monkeypatch


@pytest.fixture()
def jintrac_env_serial(monkeypatch, users_home, runs_home, jetto_exe_serial):
    monkeypatch.setenv('USERS_HOME', users_home.strpath)
    monkeypatch.setenv('RUNS_HOME', runs_home.strpath)

    return monkeypatch


@pytest.fixture()
def processes(fake_process, jetto_source_dir, jetto_exe):
    stdout = (f' JETTO  GIT repository : {jetto_source_dir.strpath}\n'
              ' JETTO  SHA1-key       : f425ed9c4cb8b20c6698e3bcb5a8faf8bf61dc55\n'
              'FORTRAN STOP\n')

    fake_process.register_subprocess([jetto_exe.strpath, fake_process.any()],
                                     stdout=[stdout],
                                     returncode=0)

    fake_process.register_subprocess(['batch_submit'],
                                     stdout='llsubmit',
                                     returncode=0,
                                     occurrences=100)

    fake_process.register_subprocess(['llsubmit', fake_process.any()],
                                     stdout='',
                                     returncode=0,
                                     occurrences=100)

    return fake_process


@pytest.fixture()
def processes_serial(fake_process, jetto_source_dir, jetto_exe_serial):
    stdout = (f' JETTO  GIT repository : {jetto_source_dir.strpath}\n'
              ' JETTO  SHA1-key       : f425ed9c4cb8b20c6698e3bcb5a8faf8bf61dc55\n'
              'FORTRAN STOP\n')

    fake_process.register_subprocess([jetto_exe_serial.strpath, fake_process.any()],
                                     stdout=[stdout],
                                     returncode=0)

    fake_process.register_subprocess(['batch_submit'],
                                     stdout='llsubmit',
                                     returncode=0,
                                     occurrences=100)

    fake_process.register_subprocess(['llsubmit', fake_process.any()],
                                     stdout='',
                                     returncode=0,
                                     occurrences=100)

    return fake_process


@pytest.fixture()
def failing_jetto_exe_process(fake_process, jetto_exe):
    fake_process.register_subprocess([jetto_exe.strpath, fake_process.any()],
                                     stdout=[''],
                                     returncode=127)


@pytest.fixture()
def failing_batch_submit_process(fake_process, jetto_source_dir, jetto_exe):
    stdout = (f' JETTO  GIT repository : {jetto_source_dir.strpath}\n'
              ' JETTO  SHA1-key       : f425ed9c4cb8b20c6698e3bcb5a8faf8bf61dc55\n'
              'FORTRAN STOP\n')

    fake_process.register_subprocess([jetto_exe.strpath, fake_process.any()],
                                     stdout=[stdout],
                                     returncode=0)

    fake_process.register_subprocess(['batch_submit'],
                                     stdout='llsubmit',
                                     returncode=127)

    return fake_process


@pytest.fixture()
def failing_llsubmit_process(fake_process, jetto_source_dir, jetto_exe):
    stdout = (f' JETTO  GIT repository : {jetto_source_dir.strpath}\n'
              ' JETTO  SHA1-key       : f425ed9c4cb8b20c6698e3bcb5a8faf8bf61dc55\n'
              'FORTRAN STOP\n')

    fake_process.register_subprocess([jetto_exe.strpath, fake_process.any()],
                                     stdout=[stdout],
                                     returncode=0)

    fake_process.register_subprocess(['batch_submit'],
                                     stdout='llsubmit',
                                     returncode=0)

    fake_process.register_subprocess(['llsubmit', fake_process.any()],
                                     stdout='',
                                     returncode=127,
                                     occurrences=100)

    return fake_process


class TestSubmitToBatch:
    @pytest.fixture(autouse=True)
    def mock_job(self, mocker):
        return mocker.patch('jetto_tools.job.Job')

    def test_raises_if_user_home_env_var_not_defined(self, manager, mock_config, jintrac_env, run_root,
                                                     rundir, jetto_sources):
        jintrac_env.delenv("USERS_HOME", raising=False)

        with pytest.raises(job.JobManagerError):
            manager.submit_job_to_batch(mock_config, rundir)

    @pytest.mark.skip()
    def test_raises_if_jetto_exe_does_not_exist(self, manager, mock_config, jetto_exe, run_root, jetto_sources,
                                                rundir):
        jetto_exe.remove()

        with pytest.raises(job.JobManagerError):
            manager.submit_job_to_batch(mock_config, rundir)

    def test_calls_jetto_exe_with_version_flag(self, manager, mock_config, jintrac_env, jetto_exe,
                                               rundir, processes, run_root, jetto_sources):
        manager.submit_job_to_batch(mock_config, rundir)

        assert [f'{jetto_exe.strpath}', '-v'] in processes.calls

    def test_calls_serial_jetto_exe_with_version_flag(self, manager, mock_config, jintrac_env_serial, jetto_exe_serial,
                                                      rundir, processes_serial, run_root, jetto_sources):
        mock_config.processors = 1

        manager.submit_job_to_batch(mock_config, rundir)

        assert [f'{jetto_exe_serial.strpath}', '-v'] in processes_serial.calls

    def test_raises_if_call_to_jetto_exe_fails(self, manager, mock_config, jintrac_env, failing_jetto_exe_process,
                                               rundir, run_root, jetto_sources):
        with pytest.raises(job.JobManagerError):
            manager.submit_job_to_batch(mock_config, rundir)

    @pytest.mark.parametrize('return_value', ['',
                                              'JETTO',
                                              'JETTO GIT',
                                              'JETTO GIT repository',
                                              'JETTO GIT repository: '])
    def test_raises_if_output_from_jetto_exe_cannot_be_parsed(self, manager, mock_config, jintrac_env, jetto_exe,
                                                              rundir, fake_process, run_root, jetto_sources,
                                                              return_value):
        fake_process.register_subprocess([jetto_exe.strpath, fake_process.any()],
                                         stdout=[return_value],
                                         returncode=0)

        with pytest.raises(job.JobManagerError):
            manager.submit_job_to_batch(mock_config, rundir)

    def test_exports_configuration_to_run_directory(self, manager, mock_config, jintrac_env,
                                                    rundir, processes, run_root, jetto_sources):
        manager.submit_job_to_batch(mock_config, rundir)

        mock_config.export.assert_called_once_with(os.path.join(run_root.strpath, rundir), rundir)

    def test_raises_if_jetto_run_script_does_not_exist(self,  manager, mock_config, jintrac_env,
                                                       rundir, processes, run_root, jetto_sources,
                                                       jetto_run_script):
        jetto_run_script.remove()

        with pytest.raises(job.JobManagerError):
            manager.submit_job_to_batch(mock_config, rundir)

    def test_creates_jetto_run_script_in_run_directory(self, manager, mock_config, jintrac_env,
                                                       rundir, processes, run_root, jetto_sources):
        manager.submit_job_to_batch(mock_config, rundir)

        assert os.path.isfile(os.path.join(run_root.strpath, rundir, 'rjettov'))

    @pytest.fixture()
    def pointdirs(self, run_root):
        point_001 = run_root.mkdir('point_001')
        point_002 = run_root.mkdir('point_002')
        point_003 = run_root.mkdir('point_003')

        return [point_001.strpath, point_002.strpath, point_003.strpath]

    def test_creates_jetto_run_script_in_point_run_directories(self, manager, jintrac_env, mock_config, pointdirs,
                                                               rundir, processes, run_root, jetto_sources):
        mock_config.export.return_value = pointdirs

        manager.submit_job_to_batch(mock_config, rundir)

        assert all([os.path.isfile(os.path.join(pointdir, 'rjettov')) for pointdir in pointdirs])

    def test_copies_jetto_run_script_to_run_directory(self, manager, mock_config, jintrac_env,
                                                      rundir, processes, run_root, jetto_sources,
                                                      jetto_run_script):
        manager.submit_job_to_batch(mock_config, rundir)

        with open(os.path.join(run_root.strpath, rundir, 'rjettov')) as f:
            actual_contents = f.read()
        with open(jetto_run_script) as f:
            expected_contents = f.read()

        assert actual_contents == expected_contents

    def test_jetto_run_script_permissions(self, manager, mock_config, jintrac_env,
                                          rundir, processes, run_root, jetto_sources,
                                          jetto_run_script):
        manager.submit_job_to_batch(mock_config, rundir)

        new_stat = os.stat(os.path.join(run_root.strpath, rundir, 'rjettov'))
        original_stat = os.stat(jetto_run_script.strpath)

        assert original_stat.st_mode == new_stat.st_mode

    def test_copies_jetto_run_script_to_point_run_directories(self, manager, mock_config, jintrac_env, pointdirs,
                                                              rundir, processes, run_root, jetto_sources,
                                                              jetto_run_script):
        mock_config.export.return_value = pointdirs

        manager.submit_job_to_batch(mock_config, rundir)

        for pointdir in pointdirs:
            with open(os.path.join(pointdir, 'rjettov')) as f:
                actual_contents = f.read()
            with open(jetto_run_script.strpath) as f:
                expected_contents = f.read()

            assert actual_contents == expected_contents

    def test_no_error_if_utils_script_does_not_exist(self,  manager, mock_config, jintrac_env,
                                                     processes, run_root, jetto_sources,
                                                     jetto_utils_script):
        jetto_utils_script.remove()

        manager.submit_job_to_batch(mock_config, run_root.strpath)

    def test_creates_jetto_utils_script_in_run_directory(self, manager, mock_config, jintrac_env,
                                                         rundir, processes, run_root, jetto_sources):
        manager.submit_job_to_batch(mock_config, rundir)

        assert os.path.isfile(os.path.join(run_root.strpath, rundir, 'utils'))

    def test_creates_jetto_utils_script_in_point_run_directories(self, manager, jintrac_env, mock_config, pointdirs,
                                                                 rundir, processes, run_root, jetto_sources):
        mock_config.export.return_value = pointdirs

        manager.submit_job_to_batch(mock_config, rundir)

        assert all([os.path.isfile(os.path.join(pointdir, 'utils')) for pointdir in pointdirs])

    def test_jetto_utils_script_permissions(self, manager, mock_config, jintrac_env,
                                            rundir, processes, run_root, jetto_sources,
                                            jetto_utils_script):
        manager.submit_job_to_batch(mock_config, rundir)

        new_stat = os.stat(os.path.join(run_root.strpath, rundir, 'utils'))
        original_stat = os.stat(jetto_utils_script.strpath)

        assert original_stat.st_mode == new_stat.st_mode

    def test_copies_jetto_utils_script_to_run_directory(self, manager, mock_config, jintrac_env,
                                                        rundir, processes, run_root, jetto_sources,
                                                        jetto_utils_script):
        manager.submit_job_to_batch(mock_config, rundir)

        with open(os.path.join(run_root.strpath, rundir, 'utils')) as f:
            actual_contents = f.read()
        with open(jetto_utils_script.strpath) as f:
            expected_contents = f.read()

        assert actual_contents == expected_contents

    def test_copies_jetto_utils_script_to_point_run_directories(self, manager, mock_config, jintrac_env, pointdirs,
                                                                rundir, processes, run_root, jetto_sources,
                                                                jetto_utils_script):
        mock_config.export.return_value = pointdirs

        manager.submit_job_to_batch(mock_config, rundir)

        for pointdir in pointdirs:
            with open(os.path.join(pointdir, 'utils')) as f:
                actual_contents = f.read()
            with open(jetto_utils_script.strpath) as f:
                expected_contents = f.read()

            assert actual_contents == expected_contents

    def test_creates_batchfile_parallel_run(self, manager, mock_config, jintrac_env, processes,
                                            rundir, run_root, jetto_sources):
        manager.submit_job_to_batch(mock_config, rundir)

        assert os.path.isfile(run_root.join(rundir, '.llcmd'))

    def test_batchfile_contents_parallel_run(self, manager, mock_config, jintrac_env, processes,
                                             rundir, run_root, jetto_sources):
        mock_config.processors = 4

        manager.submit_job_to_batch(mock_config, rundir)
        with open(run_root.join(rundir, '.llcmd'), 'r') as f:
            batchfile_contents = f.read()

        assert batchfile_contents == '\n'.join(['#!/bin/sh',
                                                f'# @ job_name = jetto.{rundir.replace("/", ".")}',
                                                '# @ input = /dev/null',
                                                '# @ output = ll.out',
                                                '# @ error = ll.err',
                                                '# @ restart = no',
                                                '# @ checkpoint = no',
                                                '# @ environment = COPY_ALL',
                                                '# @ jobtype = openmpi',
                                                f'# @ min_processors = {mock_config.processors}',
                                                f'# @ max_processors = {mock_config.processors}',
                                                '',
                                                f'# @ initialdir = {run_root.join(rundir).strpath}',
                                                f'# @ executable = {os.path.join(run_root.join(rundir).strpath, "rjettov")}',
                                                f'# @ arguments = -S -p -xmpi -x64 {rundir} '
                                                f'{mock_config.binary} {mock_config.userid}',
                                                '# @ queue',
                                                '',
                                                ''])

    def test_batchfile_contents_serial_run(self, manager, mock_config, jintrac_env_serial, processes_serial,
                                           rundir, run_root, jetto_sources):
        mock_config.processors = 1

        manager.submit_job_to_batch(mock_config, rundir)
        with open(run_root.join(rundir, '.llcmd'), 'r') as f:
            batchfile_contents = f.read()

        assert batchfile_contents == '\n'.join(['#!/bin/sh',
                                                f'# @ job_name = jetto.{rundir.replace("/", ".")}',
                                                '# @ input = /dev/null',
                                                '# @ output = ll.out',
                                                '# @ error = ll.err',
                                                '# @ restart = no',
                                                '# @ checkpoint = no',
                                                '# @ environment = COPY_ALL',
                                                '',
                                                f'# @ initialdir = {run_root.join(rundir).strpath}',
                                                f'# @ executable = {os.path.join(run_root.join(rundir).strpath, "rjettov")}',
                                                f'# @ arguments = -S -p -x64 {rundir} '
                                                f'{mock_config.binary} {mock_config.userid}',
                                                '# @ queue',
                                                '',
                                                ''])

    def test_creates_batchfiles_in_point_run_directories(self, manager, mock_config, jintrac_env, pointdirs,
                                                         rundir, processes, run_root, jetto_sources,
                                                         jetto_utils_script):
        mock_config.export.return_value = pointdirs

        manager.submit_job_to_batch(mock_config, rundir)

        for pointdir in pointdirs:
            assert os.path.isfile(os.path.join(pointdir, '.llcmd'))

    def test_batchfile_job_name_in_point_directories(self, manager, mock_config, jintrac_env, pointdirs,
                                                     rundir, processes, run_root, jetto_sources,
                                                     jetto_utils_script):
        mock_config.export.return_value = pointdirs

        manager.submit_job_to_batch(mock_config, rundir)

        for pointdir in pointdirs:
            batchfile = os.path.join(pointdir, '.llcmd')

            relpath = os.path.relpath(pointdir, start=run_root.strpath)

            with open(batchfile) as f:
                contents = f.read()

            assert f'job_name = jetto.{relpath.replace("/", ".")}' in contents

    def test_does_not_submit_run_if_not_required(self, manager, mock_config, jintrac_env, processes,
                                                 rundir, run_root, jetto_sources):
        llcmd = os.path.join(run_root.strpath, rundir, '.llcmd')
        manager.submit_job_to_batch(mock_config, rundir, run=False)

        assert [f'llsubmit', f'{llcmd}'] not in processes.calls

    def test_submits_run_if_required(self, manager, mock_config, jintrac_env, processes,
                                     rundir, run_root, jetto_sources):
        llcmd = os.path.join(run_root.strpath, rundir, '.llcmd')
        manager.submit_job_to_batch(mock_config, rundir, run=True)

        assert [f'llsubmit', f'{llcmd}'] in processes.calls

    def test_submits_runs_for_multiple_points_if_required(self, manager, mock_config, jintrac_env,
                                                          rundir, processes, run_root, pointdirs, jetto_sources):
        mock_config.export.return_value = pointdirs
        llcmds = [os.path.join(pointdir, '.llcmd') for pointdir in pointdirs]

        manager.submit_job_to_batch(mock_config, rundir, run=True)

        assert all([['llsubmit', f'{llcmd}'] in processes.calls
                    for llcmd in llcmds])

    def test_raises_if_runs_home_env_var_missing(self, manager, mock_config, jintrac_env, processes,
                                                 rundir, run_root, jetto_sources):
        jintrac_env.delenv('RUNS_HOME')

        with pytest.raises(job.JobManagerError):
            manager.submit_job_to_batch(mock_config, rundir, run=True)

    def test_raises_if_batch_submit_command_fails(self, manager, mock_config, jintrac_env,
                                                  rundir, failing_batch_submit_process, run_root, jetto_sources):
        with pytest.raises(job.JobManagerError):
            manager.submit_job_to_batch(mock_config, rundir, run=True)

    def test_raises_if_batch_submit_fails(self, manager, mock_config, jintrac_env, failing_llsubmit_process,
                                          rundir, run_root, jetto_sources):
        with pytest.raises(job.JobManagerError):
            manager.submit_job_to_batch(mock_config, rundir, run=True)

    def test_creates_job_corresponding_to_rundir(self, manager, mock_config, jintrac_env, processes,
                                                 rundir, run_root, jetto_sources, mock_job):
        _ = manager.submit_job_to_batch(mock_config, rundir)

        mock_job.assert_called_once_with(os.path.join(run_root, rundir))

    def test_creates_multiple_jobs_corresponding_to_rundirs(self, manager, mock_config, jintrac_env, rundir, processes,
                                                            run_root, pointdirs, jetto_sources, mock_job, mocker):
        mock_config.export.return_value = pointdirs

        _ = manager.submit_job_to_batch(mock_config, rundir)

        assert all(mocker.call(p) in mock_job.mock_calls for p in pointdirs)

    def test_returns_job_associated_with_single_point(self, manager, mock_config, jintrac_env, processes,
                                                      rundir, run_root, jetto_sources, mock_job):
        mock_job.return_value = 1

        jobs = manager.submit_job_to_batch(mock_config, rundir)

        assert jobs == [1]

    def test_returns_job_associated_with_multiple_points(self, manager, mock_config, jintrac_env, rundir, processes,
                                                         run_root, pointdirs, jetto_sources, mock_job, mocker):
        mock_config.export.return_value = pointdirs
        mock_job.side_effect = [1, 2, 3]

        jobs = manager.submit_job_to_batch(mock_config, rundir)

        assert jobs == [1, 2, 3]


@pytest.fixture()
def mock_prominence_client():
    return mock.Mock(spec=prominence.client.ProminenceClient)


@pytest.fixture()
def mock_prominence(mock_prominence_client):
    with mock.patch('jetto_tools.job.prominence.client.ProminenceClient',
                    autospec=prominence.client.ProminenceClient) as _fixture:
        _fixture.return_value = mock_prominence_client

        yield _fixture


class TestSubmitSingleRunToProminence:
    """Test that we can submit a JETTO job to the PROMINENCE system"""
    @pytest.fixture()
    def export(self):
        """Create three job files in the export directory"""
        def _fixture(path):
            for i in range(3):
                with open(os.path.join(path, f'file{i}.txt'), 'w') as f:
                    pass

        return _fixture

    def compare_dirs(self, original, tarball):
        result = True
        cmp = filecmp.dircmp(original, tarball)

        if cmp.common == cmp.right_list:
            for file in cmp.common:
                first_file = os.path.join(original, file)
                second_file = os.path.join(tarball, file)
                if not filecmp.cmp(first_file, second_file, shallow=False):
                    result = False
        else:
            result = False
        return result

    def test_exports_configuration_to_run_directory(self, mock_prominence, manager, mock_config, jintrac_env,
                                                    rundir, run_root):
        manager.submit_job_to_prominence(mock_config, rundir)

        mock_config.export.assert_called_once_with(os.path.join(run_root.strpath, rundir), rundir)

    def test_prominence_authenticated_client_created(self, mock_prominence, manager, mock_config, jintrac_env,
                                                     rundir, run_root):
        manager.submit_job_to_prominence(mock_config, rundir)

        mock_prominence.assert_called_once_with(authenticated=True)

    def test_prominence_upload_called(self, mock_prominence, manager, mock_config, jintrac_env,
                                      rundir, run_root, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, rundir)

        mock_prominence_client.upload.assert_called_once()

    @pytest.mark.parametrize('run_dir, expected_tarball_pattern',
                             [('foo', r'foo-[0-9a-fA-F\-]+\.tgz'),
                              ('foo/bar', r'foo\-bar[0-9a-fA-F\-]+\.tgz')],
                             ids=['Single directory', 'Nested directory'])
    def test_tarball_name_format(self, mock_prominence, manager, mock_config, jintrac_env,
                                 run_root, run_dir, expected_tarball_pattern, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, run_dir)

        actual_tarball_name = mock_prominence_client.upload.call_args[0][0]

        assert re.fullmatch(expected_tarball_pattern, actual_tarball_name)

    def test_tarball_files_are_subset_of_rundir(self, mock_prominence, manager, mock_config, jintrac_env,
                                                run_root, rundir, tar_extract_dir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, rundir)

        tarball_path = mock_prominence_client.upload.call_args[0][1]
        with tarfile.open(tarball_path) as tarball:
            tarball.extractall(path=tar_extract_dir.strpath)

        assert self.compare_dirs(os.path.join(run_root.strpath, rundir), os.path.join(tar_extract_dir.strpath, rundir))

    def test_jset_excluded_from_tarball(self, mock_prominence, manager, mock_config, jintrac_env,
                                        run_root, rundir, tar_extract_dir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, rundir)

        tarball_path = mock_prominence_client.upload.call_args[0][1]
        with tarfile.open(tarball_path) as tarball:
            tarball.extractall(path=tar_extract_dir.strpath)

        assert all('jetto.jset' not in files for _1, _2, files in
                   os.walk(os.path.join(tar_extract_dir.strpath, rundir)))

    @pytest.mark.parametrize('side_effect', [ConnectionError,
                                             AuthenticationError,
                                             FileUploadError])
    def test_raises_if_upload_fails(self, mock_prominence, manager, mock_config, jintrac_env,
                                    run_root, rundir, side_effect, mock_prominence_client):
        mock_prominence_client.upload.side_effect = side_effect

        with pytest.raises(job.JobManagerError):
            manager.submit_job_to_prominence(mock_config, rundir)

    def test_raises_if_walltime_is_empty(self, mock_prominence, manager, mock_config, jintrac_env,
                                         run_root, rundir, mock_prominence_client):
        mock_config.walltime = None

        with pytest.raises(job.JobManagerError):
            manager.submit_job_to_prominence(mock_config, rundir)

    def test_prominence_create_job_called(self, mock_prominence, manager, mock_config, jintrac_env,
                                          run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, rundir)

        mock_prominence_client.create_job.assert_called_once()

    @pytest.mark.parametrize('side_effect', [ConnectionError,
                                             AuthenticationError,
                                             FileUploadError])
    def test_raises_if_create_job_fails(self, mock_prominence, manager, mock_config, jintrac_env,
                                        run_root, rundir, mock_prominence_client, side_effect):
        mock_prominence_client.create_job.side_effect = side_effect

        with pytest.raises(job.JobManagerError):
            manager.submit_job_to_prominence(mock_config, rundir)

    @pytest.mark.parametrize('run_dir, expected_name',
                             [('foo', 'foo'),
                              ('foo/bar', 'foo-bar')],
                             ids=['Single directory', 'Nested directory'])
    def test_job_name_has_expected_value(self, mock_prominence, manager, mock_config, jintrac_env,
                                         run_root, mock_prominence_client, run_dir, expected_name):
        manager.submit_job_to_prominence(mock_config, run_dir)

        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert job_['name'] == expected_name

    def test_job_task_has_single_dict(self, mock_prominence, manager, mock_config, jintrac_env,
                                      run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, rundir)
        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert len(job_['tasks']) == 1 and isinstance(job_['tasks'][0], dict)

    @pytest.mark.parametrize('processors, cmd', [(1, 'rjettov -x64 -S prom build docker'),
                                                 (2, 'rjettov -xmpi -x64 -S prom build docker')],
                             ids=['Serial', 'Parallel'])
    def test_job_task_cmd_has_expected_values(self, mock_prominence, manager, mock_config, jintrac_env,
                                              run_root, rundir, mock_prominence_client, processors, cmd):
        mock_config.processors = processors

        manager.submit_job_to_prominence(mock_config, rundir)
        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert job_['tasks'][0]['cmd'] == cmd

    @pytest.mark.parametrize('userid, binary, image', [('sim', 'v060619', 'CCFE/JINTRAC/sim:v060619.tgz'),
                                                       ('foo', 'bar', 'CCFE/JINTRAC/foo:bar.tgz')])
    def test_job_task_image_has_expected_values(self, mock_prominence, manager, mock_config, jintrac_env,
                                                run_root, rundir, mock_prominence_client, userid, binary, image):
        mock_config.userid = userid
        mock_config.binary = binary

        manager.submit_job_to_prominence(mock_config, rundir)
        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert job_['tasks'][0]['image'] == image

    def test_job_task_runtime_is_udocker(self, mock_prominence, manager, mock_config, jintrac_env,
                                         run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, rundir)
        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert job_['tasks'][0]['runtime'] == 'udocker'

    @pytest.mark.parametrize('cpus', [1, 2], ids=['Serial', 'Parallel'])
    def test_job_resources_cpus_has_expected_value(self, mock_prominence, manager, mock_config, jintrac_env,
                                                   run_root, rundir, mock_prominence_client, cpus):
        mock_config.processors = cpus

        manager.submit_job_to_prominence(mock_config, rundir)
        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert job_['resources']['cpus'] == cpus

    @pytest.mark.parametrize('cpus, memory', [(1, 6),
                                              (2, 6),
                                              (3, 6),
                                              (4, 8)])
    def test_job_resources_memory_has_expected_value(self, mock_prominence, manager, mock_config, jintrac_env,
                                                     run_root, rundir, mock_prominence_client, cpus, memory):
        mock_config.processors = cpus

        manager.submit_job_to_prominence(mock_config, rundir)
        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert job_['resources']['memory'] == memory

    def test_job_resources_disk_has_expected_value(self, mock_prominence, manager, mock_config, jintrac_env,
                                                   run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, rundir)
        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert job_['resources']['disk'] == 10 and job_['resources']['nodes'] == 1

    @pytest.mark.parametrize('in_walltime, out_walltime', [(0, 0), (1, 60), (1.5, 90)])
    def test_job_resources_walltime_has_expected_value(self, mock_prominence, manager, mock_config, jintrac_env,
                                                       run_root, rundir, mock_prominence_client, in_walltime,
                                                       out_walltime):
        mock_config.walltime = in_walltime

        manager.submit_job_to_prominence(mock_config, rundir)
        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert job_['resources']['walltime'] == out_walltime

    def test_job_raises_if_walltime_is_empty(self, mock_prominence, manager, mock_config, jintrac_env,
                                             run_root, rundir, mock_prominence_client):
        mock_config.walltime = None

        with pytest.raises(job.JobManagerError):
            manager.submit_job_to_prominence(mock_config, rundir)

    def test_job_artifacts_has_single_dict(self, mock_prominence, manager, mock_config, jintrac_env,
                                           run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, rundir)
        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert len(job_['artifacts']) == 1 and isinstance(job_['artifacts'][0], dict)

    def test_job_artifacts_url_is_set_to_tarball(self, mock_prominence, manager, mock_config, jintrac_env,
                                                 run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, rundir)

        tarball_path = mock_prominence_client.upload.call_args[0][1]
        tarball = os.path.basename(tarball_path)
        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert job_['artifacts'][0]['url'] == tarball

    def test_job_artifact_mountpoint_contains_rundir(self, mock_prominence, manager, mock_config, jintrac_env,
                                                     run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, rundir)

        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert job_['artifacts'][0]['mountpoint'] == f'{rundir}:/jetto/runs/prom'

    def test_job_labels_app_has_expected_value(self, mock_prominence, manager, mock_config, jintrac_env,
                                               run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, rundir)

        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert job_['labels']['app'] == 'jintrac'

    def test_job_labels_fullpath_has_expected_value(self, mock_prominence, manager, mock_config, jintrac_env,
                                                    run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, rundir)

        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert job_['labels']['fullpath'] == os.path.join(run_root.strpath, rundir)

    def test_job_labels_codeid_has_expected_value(self, mock_prominence, manager, mock_config, jintrac_env,
                                                  run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, rundir)

        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert job_['labels']['codeid'] == 'jetto'

    def test_job_output_dirs_has_expected_value(self, mock_prominence, manager, mock_config, jintrac_env,
                                                run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, rundir)

        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert job_['outputDirs'] == [rundir]

    def test_job_notifications_has_expected_value(self, mock_prominence, manager, mock_config, jintrac_env,
                                                  run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, rundir)

        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert job_['notifications'] == [{'event': 'jobFinished', 'type': 'email'}]

    def test_job_policies_has_expected_value(self, mock_prominence, manager, mock_config, jintrac_env,
                                             run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_config, rundir)

        job_ = mock_prominence_client.create_job.call_args[0][0]

        assert job_['policies'] == {'maximumTimeInQueue': 7 * 24 * 60, 'leaveInQueue': True, 'autoScalingType': None}

    def test_prominence_job_id_is_returned(self, mock_prominence, manager, mock_config, jintrac_env,
                                           run_root, rundir, mock_prominence_client):
        mock_prominence_client.create_job.return_value = 1234

        id = manager.submit_job_to_prominence(mock_config, rundir)

        assert id == 1234

    def test_creates_file_recording_job_id(self, mock_prominence, manager, mock_config, jintrac_env,
                                           run_root, rundir, mock_prominence_client):
        mock_prominence_client.create_job.return_value = 1234

        _ = manager.submit_job_to_prominence(mock_config, rundir)

        with open(os.path.join(run_root.strpath, rundir, 'remote.jobid'), 'r', encoding='utf-8') as f:
            assert f.read() == 'Job submitted with id 1234\n'


class TestSubmitScanToProminence:
    """Test that we can submit a JETTO scan workflow to the PROMINENCE system"""

    @pytest.fixture()
    def mock_export(self, run_root):
        """Create three dummy files in three point directories"""

        def _export(_self, run_dir):
            pointdirs = []
            for point in range(3):
                run_path = os.path.join(run_root.strpath, run_dir, f'point_00{point}')
                if not os.path.isdir(run_path):
                    os.makedirs(run_path, exist_ok=True)

                for file in ('jetto.jset', 'jetto.in', 'serialisation.json'):
                    with open(os.path.join(run_path, file), 'wt') as f:
                        f.write(file)

                pointdirs.append(run_path)

            return pointdirs

        return _export

    @pytest.fixture()
    def mock_scan_config(self, run_root, mock_export):
        m = mock.MagicMock(spec=jetto_tools.config.RunConfig)
        m.userid = 'sim'
        m.binary = 'v060619'
        m.processors = 2
        m.walltime = 2
        m._npoints.return_value = 3
        m.export.side_effect = mock_export

        return m

    def compare_dir_trees(self, original, new, ignore):
        """Recursively compare the original and tarballed directory tree

        Adapted from https://stackoverflow.com/a/6681395
        """
        dirs_cmp = filecmp.dircmp(original, new, ignore=ignore)
        if len(dirs_cmp.left_only) > 0 or len(dirs_cmp.right_only) > 0 or \
                len(dirs_cmp.funny_files) > 0:
            return False
        (_, mismatch, errors) = filecmp.cmpfiles(
            original, new, dirs_cmp.common_files, shallow=False)
        if len(mismatch) > 0 or len(errors) > 0:
            return False
        for common_dir in dirs_cmp.common_dirs:
            new_dir1 = os.path.join(original, common_dir)
            new_dir2 = os.path.join(new, common_dir)
            if not self.compare_dir_trees(new_dir1, new_dir2, ignore=ignore):
                return False

        return True

    def test_exports_configuration_to_run_directory(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                    rundir, run_root):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        mock_scan_config.export.assert_called_once_with(os.path.join(run_root.strpath, rundir), rundir)

    def test_prominence_authenticated_client_created(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                     rundir, run_root):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        mock_prominence.assert_called_once_with(authenticated=True)

    def test_prominence_upload_called(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                      rundir, run_root, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        mock_prominence_client.upload.assert_called_once()

    @pytest.mark.parametrize('run_dir, expected_tarball_pattern',
                             [('foo', r'foo-[0-9a-fA-F\-]+\.tgz'),
                              ('foo/bar', r'foo\-bar[0-9a-fA-F\-]+\.tgz')],
                             ids=['Single directory', 'Nested directory'])
    def test_tarball_name_format(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                 run_root, run_dir, expected_tarball_pattern, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, run_dir)

        actual_tarball_name = mock_prominence_client.upload.call_args[0][0]

        assert re.fullmatch(expected_tarball_pattern, actual_tarball_name)

    def test_tarball_files_match_rundir_contents(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                 run_root, rundir, tar_extract_dir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        tarball_path = mock_prominence_client.upload.call_args[0][1]
        with tarfile.open(tarball_path) as tarball:
            tarball.extractall(path=tar_extract_dir.strpath)

        assert self.compare_dir_trees(os.path.join(run_root.strpath, rundir),
                                      os.path.join(tar_extract_dir.strpath, rundir),
                                      ignore=['remote.jobid', 'jetto.jset'])

    def test_tarball_files_match_nested_rundir_contents(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                        run_root, tar_extract_dir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, 'foo/bar')

        tarball_path = mock_prominence_client.upload.call_args[0][1]
        with tarfile.open(tarball_path) as tarball:
            tarball.extractall(path=tar_extract_dir.strpath)

        assert self.compare_dir_trees(os.path.join(run_root.strpath, 'foo/bar'),
                                      os.path.join(tar_extract_dir.strpath, 'bar'),
                                      ignore=['remote.jobid', 'jetto.jset'])

    def test_jset_files_excluded_from_tarball(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                              run_root, rundir, tar_extract_dir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        tarball_path = mock_prominence_client.upload.call_args[0][1]
        with tarfile.open(tarball_path) as tarball:
            tarball.extractall(path=tar_extract_dir.strpath)

        assert all('jetto.jset' not in files for _1, _2, files in
                   os.walk(os.path.join(tar_extract_dir.strpath, rundir)))

    @pytest.mark.parametrize('side_effect', [ConnectionError,
                                             AuthenticationError,
                                             FileUploadError])
    def test_raises_if_upload_fails(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                    run_root, rundir, side_effect, mock_prominence_client):
        mock_prominence_client.upload.side_effect = side_effect

        with pytest.raises(job.JobManagerError):
            manager.submit_job_to_prominence(mock_scan_config, rundir)

    def test_prominence_create_workflow(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                        run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        mock_prominence_client.create_workflow.assert_called_once()

    @pytest.mark.parametrize('side_effect', [ConnectionError,
                                             AuthenticationError,
                                             WorkflowCreationError])
    def test_raises_if_create_workflow_fails(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                             run_root, rundir, mock_prominence_client, side_effect):
        mock_prominence_client.create_workflow.side_effect = side_effect

        with pytest.raises(job.JobManagerError):
            manager.submit_job_to_prominence(mock_scan_config, rundir)

    @pytest.mark.parametrize('run_dir, expected_name',
                             [('foo', 'foo'),
                              ('foo/bar', 'foo-bar')],
                             ids=['Single directory', 'Nested directory'])
    def test_workflow_name_has_expected_value(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                              run_root, mock_prominence_client, run_dir, expected_name):
        manager.submit_job_to_prominence(mock_scan_config, run_dir)

        workflow = mock_prominence_client.create_workflow.call_args[0][0]

        assert workflow['name'] == expected_name

    def test_workflow_has_single_job(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                     run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)
        jobs = mock_prominence_client.create_workflow.call_args[0][0]['jobs']

        assert len(jobs) == 1

    def test_workflow_job_tasks_has_single_task(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)
        job_ = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]

        assert len(job_['tasks']) == 1

    @pytest.mark.parametrize('processors, cmd', [(1, 'rjettov -x64 -S $workdir build docker'),
                                                 (2, 'rjettov -xmpi -x64 -S $workdir build docker')],
                             ids=['Serial', 'Parallel'])
    def test_workflow_task_cmd_has_expected_values(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                   run_root, rundir, mock_prominence_client, processors, cmd):
        mock_scan_config.processors = processors

        manager.submit_job_to_prominence(mock_scan_config, rundir)
        task = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]['tasks'][0]

        assert task['cmd'] == cmd

    @pytest.mark.parametrize('userid, binary, image', [('sim', 'v060619', 'CCFE/JINTRAC/sim:v060619.tgz'),
                                                       ('foo', 'bar', 'CCFE/JINTRAC/foo:bar.tgz')])
    def test_workflow_task_image_has_expected_values(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                     run_root, rundir, mock_prominence_client, userid, binary, image):
        mock_scan_config.userid = userid
        mock_scan_config.binary = binary

        manager.submit_job_to_prominence(mock_scan_config, rundir)
        task = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]['tasks'][0]

        assert task['image'] == image

    def test_workflow_task_runtime_is_udocker(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                              run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)
        task = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]['tasks'][0]

        assert task['runtime'] == 'udocker'

    @pytest.mark.parametrize('cpus', [1, 2], ids=['Serial', 'Parallel'])
    def test_workflow_resources_cpus_has_expected_value(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                        run_root, rundir, mock_prominence_client, cpus):
        mock_scan_config.processors = cpus

        manager.submit_job_to_prominence(mock_scan_config, rundir)
        resources = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]['resources']

        assert resources['cpus'] == cpus

    @pytest.mark.parametrize('cpus, memory', [(1, 6),
                                              (2, 6),
                                              (3, 6),
                                              (4, 8)])
    def test_job_resources_memory_has_expected_value(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                     run_root, rundir, mock_prominence_client, cpus, memory):
        mock_scan_config.processors = cpus

        manager.submit_job_to_prominence(mock_scan_config, rundir)
        resources = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]['resources']

        assert resources['memory'] == memory

    def test_job_resources_disk_has_expected_value(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                   run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)
        resources = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]['resources']

        assert resources['disk'] == 10 and resources['nodes'] == 1

    @pytest.mark.parametrize('in_walltime, out_walltime', [(0, 0), (1, 60), (1.5, 90)])
    def test_job_resources_walltime_has_expected_value(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                       run_root, rundir, mock_prominence_client, in_walltime,
                                                       out_walltime):
        mock_scan_config.walltime = in_walltime

        manager.submit_job_to_prominence(mock_scan_config, rundir)
        resources = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]['resources']

        assert resources['walltime'] == out_walltime

    def test_job_raises_if_walltime_is_empty(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                             run_root, rundir, mock_prominence_client):
        mock_scan_config.walltime = None

        with pytest.raises(job.JobManagerError):
            manager.submit_job_to_prominence(mock_scan_config, rundir)

    def test_job_artifacts_has_single_dict(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                           run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)
        artifacts = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]['artifacts']

        assert len(artifacts) == 1

    def test_job_artifacts_url_is_set_to_tarball(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                 run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        tarball_path = mock_prominence_client.upload.call_args[0][1]
        tarball = os.path.basename(tarball_path)
        artifacts = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]['artifacts'][0]

        assert artifacts['url'] == tarball

    def test_job_artifact_mountpoint_contains_rundir(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                     run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        artifacts = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]['artifacts'][0]

        assert artifacts['mountpoint'] == f'{rundir}:/jetto/runs/prom'

    def test_job_artifact_mountpoint_is_basename_of_nested_rundir(self, mock_prominence, manager, mock_scan_config,
                                                                  jintrac_env, run_root, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, 'foo/bar')

        artifacts = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]['artifacts'][0]

        assert artifacts['mountpoint'] == 'bar:/jetto/runs/prom'

    def test_job_labels_app_has_expected_value(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                               run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        labels = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]['labels']

        assert labels['app'] == 'jintrac'

    def test_job_labels_fullpath_has_expected_value(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                    run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        labels = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]['labels']

        assert labels['fullpath'] == os.path.join(run_root.strpath, rundir)

    def test_job_labels_codeid_has_expected_value(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                  run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        labels = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]['labels']

        assert labels['codeid'] == 'jetto'

    def test_job_output_dirs_has_expected_value(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        job_ = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]

        assert job_['outputDirs'] == [rundir]

    def test_job_output_dirs_for_nested_rundir(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                               run_root, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, 'foo/bar')

        job_ = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]

        assert job_['outputDirs'] == ['bar']

    def test_job_notifications_has_expected_value(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                  run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        job_ = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]

        assert job_['notifications'] == [{'event': 'jobFinished', 'type': 'email'}]

    def test_job_policies_has_expected_value(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                             run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        job_ = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]

        assert job_['policies'] == {'maximumTimeInQueue': 7 * 24 * 60, 'leaveInQueue': True, 'autoScalingType': None}

    def test_workflow_includes_factory(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                       run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        workflow = mock_prominence_client.create_workflow.call_args[0][0]

        assert 'factories' in workflow

    def test_workflow_contains_single_factory(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                              run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        workflow = mock_prominence_client.create_workflow.call_args[0][0]

        assert isinstance(workflow['factories'], list) and len(workflow['factories']) == 1

    def test_workflow_factory_type_is_zip(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                          run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        factory = mock_prominence_client.create_workflow.call_args[0][0]['factories'][0]

        assert factory['type'] == 'zip'

    def test_workflow_factory_has_single_parameter(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                   run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        parameters = mock_prominence_client.create_workflow.call_args[0][0]['factories'][0]['parameters']

        assert len(parameters) == 1

    def test_workflow_factory_name_is_same_as_workflow(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                       run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        workflow = mock_prominence_client.create_workflow.call_args[0][0]
        factory = workflow['factories'][0]

        assert factory['name'] == workflow['name']

    def test_workflow_factory_job_name_is_same_as_workflow(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                           run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        workflow = mock_prominence_client.create_workflow.call_args[0][0]
        factory = workflow['factories'][0]

        assert factory['jobs'] == [workflow['jobs'][0]['name']]

    def test_workflow_factory_parameter_name_is_workdir(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                        run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        parameter = mock_prominence_client.create_workflow.call_args[0][0]['factories'][0]['parameters'][0]

        assert parameter['name'] == 'workdir'

    def test_workflow_factory_parameter_values_are_point_dirs(self, mock_prominence, manager, mock_scan_config,
                                                              jintrac_env, run_root, rundir, mock_prominence_client,
                                                              mock_export):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        expected_values = [os.path.join('prom', os.path.basename(path)) for path in mock_export(None, rundir)]
        parameter = mock_prominence_client.create_workflow.call_args[0][0]['factories'][0]['parameters'][0]

        assert parameter['values'] == expected_values

    def test_prominence_workflow_id_is_returned(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                run_root, rundir, mock_prominence_client):
        mock_prominence_client.create_workflow.return_value = 1234

        id = manager.submit_job_to_prominence(mock_scan_config, rundir)

        assert id == 1234

    def test_creates_file_recording_workflow_id(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                                run_root, rundir, mock_prominence_client):
        mock_prominence_client.create_workflow.return_value = 1234

        _ = manager.submit_job_to_prominence(mock_scan_config, rundir)

        with open(os.path.join(run_root.strpath, rundir, 'remote.jobid'), 'r', encoding='utf-8') as f:
            assert f.read() == 'Job submitted with id 1234\n'

    def test_workflow_name_same_as_job_name(self, mock_prominence, manager, mock_scan_config, jintrac_env,
                                            run_root, rundir, mock_prominence_client):
        manager.submit_job_to_prominence(mock_scan_config, rundir)

        workflow_name = mock_prominence_client.create_workflow.call_args[0][0]['name']
        job_name = mock_prominence_client.create_workflow.call_args[0][0]['jobs'][0]['name']

        assert workflow_name == job_name


class TestJob:
    @pytest.fixture
    def rundir(self, tmpdir):
        return tmpdir.mkdir('point_000')

    @pytest.fixture(autouse=True)
    def serialisation(self, rundir):
        f = rundir.join('serialisation.json')
        f.write(json.dumps({'foo': 'bar'}))

        return f

    @pytest.fixture(autouse=True)
    def llcmddbg(self, rundir, id):
        f = rundir.join('.llcmd.dbg')
        f.write(f'Your job {id} ("jetto.point00000") has been submitted')

        return f

    def test_raises_if_rundir_does_not_exist(self, rundir):
        rundir.remove()

        with pytest.raises(jetto_tools.job.JobError):
            _ = job.Job(rundir.strpath)

    def test_rundir_property(self, rundir):
        job_under_test = job.Job(rundir.strpath)

        assert job_under_test.rundir == rundir.strpath

    @pytest.fixture
    def id(self):
        return 12345

    def test_job_id_is_none_if_llcmd_dbg_not_found(self, rundir, llcmddbg):
        llcmddbg.remove()

        job_under_test = job.Job(rundir.strpath)

        assert job_under_test.id is None

    def test_job_id_is_retrieved_from_lldbg_file(self, rundir, id):
        job_under_test = job.Job(rundir.strpath)

        assert job_under_test.id == id

    def test_job_raises_if_llcmd_dbg_does_not_contain_id(self, rundir, llcmddbg):
        llcmddbg.write('foo')

        with pytest.raises(job.JobError):
            _ = job.Job(rundir.strpath)

    @pytest.fixture
    def jetto_out(self, rundir):
        f = rundir.join('jetto.out')
        f.write('\n'
                ' ... Terminating successfully\n'
                '\n')

        return f

    def test_job_status_unknown(self, rundir, llcmddbg, jetto_out):
        jetto_out.remove()

        job_under_test = job.Job(rundir.strpath)

        assert job_under_test.status() == job.Status.UNKNOWN

    def test_job_status_failed(self, rundir, jetto_out):
        jetto_out.write('')

        job_under_test = job.Job(rundir.strpath)

        assert job_under_test.status() == job.Status.FAILED

    def test_job_status_successful(self, rundir, jetto_out):
        job_under_test = job.Job(rundir.strpath)

        assert job_under_test.status() == job.Status.SUCCESSFUL

    def test_serialisation_property(self, rundir, serialisation):
        with open(serialisation) as f:
            d = json.loads(f.read())
        job_under_test = job.Job(rundir.strpath)

        assert job_under_test.serialisation == d

    def test_serialisation_is_none_if_not_found(self, rundir, serialisation):
        serialisation.remove()
        job_under_test = job.Job(rundir.strpath)

        assert job_under_test.serialisation is None

    def test_raises_if_serialisation_not_loaded(self, rundir, serialisation):
        serialisation.write('foo')

        with pytest.raises(job.JobError):
            _ = job.Job(rundir.strpath)


class TestRetrieveJobs:
    @pytest.fixture()
    def pointdirs(self, run_root):
        point_001 = run_root.mkdir('point_001')
        point_002 = run_root.mkdir('point_002')
        point_003 = run_root.mkdir('point_003')

        return [point_001.strpath, point_002.strpath, point_003.strpath]

    def test_returns_jobs_from_point_dirs(self, run_root, pointdirs):
        jobs = job.retrieve_jobs(run_root.strpath)

        assert [j.rundir for j in jobs] == pointdirs

    def test_raises_if_no_point_directories_found(self, run_root):
        with pytest.raises(job.JobError):
            _ = job.retrieve_jobs(run_root)

    def test_raises_if_any_job_creation_fails(self, run_root, pointdirs, mocker):
        mock = mocker.patch('jetto_tools.job.retrieve_jobs')
        mock.side_effect = jetto_tools.job.JobError

        with pytest.raises(jetto_tools.job.JobError):
            _ = job.retrieve_jobs(run_root)
