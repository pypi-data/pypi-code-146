
import os
from pathlib import Path
import re
import subprocess

import yaml


def export_env(history_only=False, include_builds=False):
    """ Capture `conda env export` output """

    cmd = ['conda', 'env', 'export']
    if history_only:
        cmd.append('--from-history')
        if include_builds:
            raise ValueError(
                'Cannot include build versions with "from history" mode')
    if not include_builds:
        cmd.append('--no-builds')
    cp = subprocess.run(cmd, stdout=subprocess.PIPE)
    try:
        cp.check_returncode()
    except:
        raise
    else:
        return yaml.safe_load(cp.stdout)


def _export_pipreqs_dep():
    ROOT_DIR = os.getcwd()
    cmd = ['pipreqs', ROOT_DIR, '--print']
    cp = subprocess.run(cmd, stdout=subprocess.PIPE)
    try:
        cp.check_returncode()
    except:
        raise
    else:
        return yaml.safe_load(cp.stdout)


def _is_history_dep(d, history_deps, prefix=False):
    if not isinstance(d, str):
        return False
    if not prefix:
        return d in history_deps
    return re.sub(r'=.*', '', d) in history_deps


def _build_pip_deps(deps_hist: list):
    try:
        pip_reqs_str = _export_pipreqs_dep()
        if not pip_reqs_str:
            raise
        deps_pipreq = {}
        make_set = set(pip_reqs_str.replace('==', '=').lower().split(' '))
        diff_set = make_set.difference(set(deps_hist))
        sort_to_list = sorted(list(diff_set))
        deps_pipreq['pip'] = sort_to_list
    except:
        raise
    finally:
        return deps_pipreq


def _combine_env_data(env_data_full, env_data_hist, envname):
    deps_full = env_data_full['dependencies']
    deps_hist = env_data_hist['dependencies']
    deps = [dep for dep in deps_full if _is_history_dep(dep, deps_hist)]
    pip_vers = [dep for dep in deps_full if _is_history_dep(
        dep, deps_hist, True)][0]

    deps.append(pip_vers)
    deps_pipreq = _build_pip_deps(deps_hist=deps_hist)

    env_data = {}

    if envname:
        env_data['name'] = envname
    else:
        env_data['name'] = env_data_full['name']

    env_data['channels'] = env_data_full['channels']
    env_data['dependencies'] = deps
    env_data['dependencies'].append(deps_pipreq)

    return env_data


def conda_env_export(filename: Path, envname: str):
    env_data_full = export_env()
    env_data_hist = export_env(history_only=True)
    env_data = _combine_env_data(env_data_full, env_data_hist, envname)
    with open(filename, "w") as f:
        yaml.dump(env_data, f)
        f.close()
