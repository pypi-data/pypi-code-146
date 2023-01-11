import json
import os
import re
import subprocess
import sys
num_processes = int(sys.argv[1])
pytest_args = sys.argv[2:]
file_timeout = int(os.environ.get('BODO_RUNTESTS_TIMEOUT', 7200))
logfile_name = 'splitting_logs/logfile-07-18-22.txt'
if 'CODEBUILD_BUILD_ID' in os.environ:
    module_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    repo_dir = os.path.abspath(os.path.join(module_dir, os.pardir))
    assert module_dir in sys.path
    if repo_dir not in sys.path:
        sys.path.append(repo_dir)
    import buildscripts.aws.select_timing_from_logs
    result = subprocess.call(['python',
        'buildscripts/aws/download_s3paths_with_prefix.py',
        'bodo-pr-testing-logs', logfile_name])
    if result != 0:
        raise Exception(
            'buildscripts/aws/download_s3_prefixes.py fails trying to download log file.'
            )
    if not os.path.exists(logfile_name):
        raise Exception('Log file download unsuccessful, exiting with failure.'
            )
    marker_groups = (buildscripts.aws.select_timing_from_logs.
        generate_marker_groups(logfile_name, int(os.environ[
        'NUMBER_GROUPS_SPLIT'])))
    with open('bodo/pytest.ini', 'a') as f:
        indent = ' ' * 4
        for marker in set(marker_groups.values()):
            print('{0}{1}: Group {1} for running distributed tests\n'.
                format(indent, marker, file=f))
    with open('testtiming.json', 'w') as f:
        json.dump(marker_groups, f)
try:
    output = subprocess.check_output(['pytest'] + pytest_args + [
        '--collect-only'])
except subprocess.CalledProcessError as e:
    if e.returncode == 5:
        exit()
    else:
        print(e.output.decode())
        raise e
pytest_module_regexp = re.compile('<Module ((?!tests/caching_tests/)\\S+.py)>')
all_modules = []
for l in output.decode().split('\n'):
    m = pytest_module_regexp.search(l)
    if m:
        filename = m.group(1).split('/')[-1]
        all_modules.append(filename)
weekly_modules = ['test_pyspark_api.py', 'test_csr_matrix.py', 'test_dl.py',
    'test_gcs.py', 'test_json.py', 'test_matplotlib.py', 'test_ml.py',
    'test_xgb.py', 'test_sklearn_part1.py', 'test_sklearn_part2.py',
    'test_sklearn_part3.py', 'test_sklearn_part4.py',
    'test_sklearn_part5.py', 'test_sklearn_linear_model.py',
    'test_sklearn_errorchecking.py', 'test_sklearn_cluster_ensemble.py',
    'test_sklearn_feature_extraction_text.py', 'test_spark_sql_str.py',
    'test_spark_sql_array.py', 'test_spark_sql_date.py',
    'test_spark_sql_numeric.py', 'test_spark_sql_map.py']
modules = list(set(all_modules) - set(weekly_modules))
codecov = '--cov-report=' in pytest_args
if codecov:
    subprocess.run(['coverage', 'erase'])
    if not os.path.exists('cov_files'):
        os.makedirs('cov_files')
tests_failed = False
for i, m in enumerate(modules):
    os.environ['BODO_TEST_PYTEST_MOD'] = m
    mod_pytest_args = list(pytest_args)
    try:
        mark_arg_idx = pytest_args.index('-m')
        mod_pytest_args[mark_arg_idx + 1] += ' and single_mod'
    except ValueError as ydl__lpw:
        mod_pytest_args += ['-m', 'single_mod']
    cmd = ['mpiexec', '-prepend-rank', '-n', str(num_processes), 'pytest',
        '-Wignore',
        f"--junitxml=pytest-report-{m.split('.')[0]}-{os.environ['PYTEST_MARKER'].replace(' ', '-')}.xml"
        ] + mod_pytest_args
    print('Running', ' '.join(cmd))
    p = subprocess.Popen(cmd, shell=False)
    rc = p.wait(timeout=file_timeout)
    if rc not in (0, 5):
        tests_failed = True
        continue
    if codecov:
        assert os.path.isfile('.coverage'), 'Coverage file was not created'
        os.rename('.coverage', './cov_files/.coverage.' + str(i))
if tests_failed:
    exit(1)
if codecov:
    subprocess.run(['coverage', 'combine', 'cov_files'])
