#!/usr/bin/env python

#
# Copyright (c) 2019-2023 Knuth Project
#

import os
import copy
import re
import platform
import importlib
import subprocess
import sys
import difflib
import tempfile
from conans import ConanFile, CMake
from conans.errors import ConanException, ConanInvalidConfiguration
from conans.model.version import Version
from conans import __version__ as conan_version

from subprocess import Popen, PIPE, STDOUT
import inspect
from collections import deque

if platform.machine() == 'x86_64':
    from microarch import get_all_data, get_all_data_from_marchid, is_superset_of, set_diff, extensions_to_names, get_compiler_flags_arch_id, level0_on, level1_on, level2_on, level3_on, encode_extensions

DEFAULT_ORGANIZATION_NAME = 'k-nuth'
DEFAULT_LOGIN_USERNAME = 'fpelliccioni'
DEFAULT_USERNAME = 'kth'
DEFAULT_REPOSITORY = 'kth'

def get_tempfile_name():
    return os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()))

def get_compilation_symbols_gcc_string_program(filename, default=None):
    ofile = filename + '.o'
    afile = filename + '.a'
    try:

        # print("get_compilation_symbols_gcc_string_program - 1")

        # g++ -D_GLIBCXX_USE_CXX11_ABI=1 -c test.cxx -o test-v2.o
        # ar cr test-v1.a test-v1.o
        # nm test-v1.a

        # g++ -D_GLIBCXX_USE_CXX11_ABI=1 -c -o ofile.o -x c++ -
        # ar cr ofile.a ofile.o
        # nm ofile.a

        p = Popen(['g++', '-D_GLIBCXX_USE_CXX11_ABI=1', '-c', '-o', ofile, '-x', 'c++', '-'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        # print("get_compilation_symbols_gcc_string_program - 2")

        output, _ = p.communicate(input=b'#include <string>\nstd::string foo __attribute__ ((visibility ("default")));\nstd::string bar __attribute__ ((visibility ("default")));\n')
        # print("get_compilation_symbols_gcc_string_program - 3")

        if p.returncode != 0:
            # print("get_compilation_symbols_gcc_string_program - 4")
            return default

        # print("get_compilation_symbols_gcc_string_program - 5")

        p = Popen(['ar', 'cr', afile, ofile], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

        # print("get_compilation_symbols_gcc_string_program - 6")
        output, _ = p.communicate()
        # print("get_compilation_symbols_gcc_string_program - 7")

        if p.returncode != 0:
            # print("get_compilation_symbols_gcc_string_program - 8")
            return default

        # print("get_compilation_symbols_gcc_string_program - 9")

        p = Popen(['nm', afile], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        # print("get_compilation_symbols_gcc_string_program - 10")
        output, _ = p.communicate()
        # print("get_compilation_symbols_gcc_string_program - 11")

        if p.returncode == 0:
            # print("get_compilation_symbols_gcc_string_program - 12")
            if output:
                # print("get_compilation_symbols_gcc_string_program - 13")
                return output.decode("utf-8")

        # print("get_compilation_symbols_gcc_string_program - 14")

        return default
    except OSError as e:
        # print("get_compilation_symbols_gcc_string_program - 15")
        print(e)
        return default
    except:
        # print("get_compilation_symbols_gcc_string_program - 16")
        return default

def get_conan_packager():
    pkg = importlib.import_module('cpt.packager')
    return pkg

def get_git_branch(default=None):
    try:
        res = subprocess.Popen(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = res.communicate()
        # print('fer 0')

        if output:
            # print('fer 0.1')
            if res.returncode == 0:
                # print('fer 0.2')
                # print(output)
                # print(output.decode("utf-8"))
                # print(output.decode("utf-8").replace('\n', ''))
                ret = output.decode("utf-8").replace('\n', '').replace('\r', '')
                # print(ret)
                return ret
        return default
    except OSError: # as e:
        # print('fer 1')
        return default
    except:
        # print('fer 2')
        return default

def get_git_describe(default=None):
    try:
        res = subprocess.Popen(["git", "describe", "master"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = res.communicate()
        if output:
            if res.returncode == 0:
                return output.decode("utf-8").replace('\n', '').replace('\r', '')
                # return output.replace('\n', '').replace('\r', '')
        return default
    except OSError: # as e:
        return default
    except:
        return default

def get_version_from_git_describe_no_releases(default=None, is_dev_branch=False):
    describe = get_git_describe()

    # print('describe')
    # print(describe)

    if describe is None:
        return None
    version = describe.split('-')[0][1:]

    if is_dev_branch:
        version_arr = version.split('.')
        if len(version_arr) != 3:
            # print('version has to be of the following format: xx.xx.xx')
            return None
        # version = "%s.%s.%s" % (version_arr[0], str(int(version_arr[1]) + 1), version_arr[2])
        version = "%s.%s.%s" % (version_arr[0], str(int(version_arr[1]) + 1), 0)

    return version

def get_version_from_git_describe(default=None, is_dev_branch=False):
    describe = get_git_describe()

    # print('describe')
    # print(describe)

    # if describe is None:
    #     return None

    if describe is None:
        describe = "v0.0.0-"

    version = describe.split('-')[0][1:]

    if is_dev_branch:
        # print(version)
        # print(release_branch_version_to_int(version))

        # print(max_release_branch())

        max_release_i, max_release_s = max_release_branch()

        if max_release_i is not None and max_release_i > release_branch_version_to_int(version):
            version = max_release_s

        version_arr = version.split('.')
        if len(version_arr) != 3:
            # print('version has to be of the following format: xx.xx.xx')
            return None
        # version = "%s.%s.%s" % (version_arr[0], str(int(version_arr[1]) + 1), version_arr[2])
        version = "%s.%s.%s" % (version_arr[0], str(int(version_arr[1]) + 1), 0)

    return version

def get_git_branches(default=None):
    try:
        # res = subprocess.Popen(["git", "branch", "-r"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # res = subprocess.Popen(["git", "branch"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # git ls-remote --heads origin
        # res = subprocess.Popen(["git", "ls-remote", "--heads"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res = subprocess.Popen(["git", "ls-remote", "--heads", "origin"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = res.communicate()
        if output:
            if res.returncode == 0:
                # return output.decode("utf-8").replace('\n', '').replace('\r', '')
                return output.decode("utf-8")
        return default
    except OSError: # as e:
        return default
    except:
        return default

def release_branch_version_to_int(version):
    verarr = version.split('.')
    if len(verarr) != 3:
        return None
    verstr = verarr[0].zfill(5) + verarr[1].zfill(5) + verarr[2].zfill(5)
    return int(verstr)

def release_branch_version(branch):
    version = branch.split('-')[-1]
    return (release_branch_version_to_int(version), version)

def max_release_branch(default=None):
    branches = get_git_branches()
    # print(branches)
    if branches is None:
        return False

    max = None
    max_str = None

    for line in branches.splitlines():
        line = line.strip()
        # print(line)
        # if line.startswith("origin/release-"):
        if "release-" in line:
            veri, vers = release_branch_version(line)
            if veri is not None:
                if max is None or veri > max:
                    max = veri
                    max_str = vers

    return (max, max_str)

def copy_env_vars(env_vars):
    env_vars["KTH_BRANCH"] = os.getenv('KTH_BRANCH', '-')
    env_vars["KTH_CONAN_CHANNEL"] = os.getenv('KTH_CONAN_CHANNEL', '-')
    env_vars["KTH_FULL_BUILD"] = os.getenv('KTH_FULL_BUILD', '-')
    env_vars["KTH_CONAN_VERSION"] = os.getenv('KTH_CONAN_VERSION', '-')

def is_development_branch_internal(branch = None):
    if branch is None:
        branch = get_branch()

    if branch is None:
        return False

    if branch == 'master':
        return False
    if branch.startswith('release'):
        return False
    if branch.startswith('hotfix'):
        return False

    return True

def is_development_branch():
    branch = get_branch()
    if branch is None:
        return False

    if branch == 'master':
        return False
    if branch.startswith('release'):
        return False
    if branch.startswith('hotfix'):
        return False

    return True

def get_branch():
    branch = os.getenv("KTH_BRANCH", None)

    if branch is None:
        branch = get_git_branch()

    return branch

def get_version_from_branch_name():
    branch = get_branch()
    if branch is None:
        return None
    if branch.startswith("release-") or branch.startswith("hotfix-"):
        return branch.split('-', 1)[1]
    if branch.startswith("release_") or branch.startswith("hotfix_"):
        return branch.split('_', 1)[1]
    return None

def option_on_off(option):
    return "ON" if option else "OFF"

def access_file(file_path):
    with open(file_path, 'r') as f:
        return f.read().replace('\n', '').replace('\r', '')

def get_content(file_name):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', file_name)
    return access_file(file_path)

def get_content_default(file_name, default=None):
    try:
        return get_content(file_name)
    except IOError as e:
        return default

def get_version_from_file(recipe_dir):
    return get_content_default_with_dir(recipe_dir, 'conan_version')

def get_version_from_file_no_recipe_dir():
    return get_content_default('conan_version')

def get_version_no_recipe_dir():
    version = get_version_from_file_no_recipe_dir()

    if version is None:
        version = os.getenv("KTH_CONAN_VERSION", None)

    if version is None:
        version = get_version_from_branch_name()

    if version is None:
        version = get_version_from_git_describe(None, is_development_branch())

    return version

def get_version(recipe_dir):
    version = get_version_from_file(recipe_dir)

    if version is None:
        version = os.getenv("KTH_CONAN_VERSION", None)

    if version is None:
        version = get_version_from_branch_name()

    if version is None:
        version = get_version_from_git_describe(None, is_development_branch())

    return version

def get_version_no_releases(recipe_dir, default=None):
    version = get_version_from_file(recipe_dir)

    if version is None:
        version = os.getenv("KTH_CONAN_VERSION", None)


    if version is None:
        version = get_version_from_branch_name()

    if version is None:
        version = get_version_from_git_describe_no_releases(None, is_development_branch())

    if version is None:
        version = default

    return version

def get_channel_from_file_no_recipe_dir():
    return get_content_default('conan_channel')

def get_channel_from_file(recipe_dir):
    return get_content_default_with_dir(recipe_dir, 'conan_channel')

def branch_to_channel(branch):
    if branch is None:
        return "staging"
    if branch == 'dev':
        return "testing"
    if branch.startswith('release'):
        return "staging"
    if branch.startswith('hotfix'):
        return "staging"
    if branch.startswith('feature'):
        return branch

    return "staging"

def get_channel_from_branch():
    return branch_to_channel(get_branch())

def get_channel_no_recipe_dir():
    channel = get_channel_from_file_no_recipe_dir()

    if channel is None:
        channel = os.getenv("KTH_CONAN_CHANNEL", None)

    if channel is None:
        # channel = get_git_branch()
        channel = get_channel_from_branch()

    if channel is None:
        channel = 'staging'

    return channel

def get_channel(recipe_dir):
    channel = get_channel_from_file(recipe_dir)

    if channel is None:
        channel = os.getenv("KTH_CONAN_CHANNEL", None)

    if channel is None:
        channel = get_channel_from_branch()

    if channel is None:
        channel = 'staging'

    return channel

def get_user(recipe_dir):
    return get_content_default_with_dir(recipe_dir, 'conan_user', DEFAULT_USERNAME)

def get_user_no_recipe_dir():
    return get_content_default('conan_user', DEFAULT_USERNAME)

def get_repository():
    return os.getenv("KTH_BINTRAY_REPOSITORY", DEFAULT_REPOSITORY)

def get_content_with_dir(dir, file_name):
    file_path = os.path.join(dir, file_name)
    return access_file(file_path)

def get_content_default_with_dir(dir, file_name, default=None):
    try:
        return get_content_with_dir(dir, file_name)
    except IOError as e:
        return default

def get_conan_req_version(recipe_dir):
    # return get_content_default('conan_req_version', None)
    return get_content_default_with_dir(recipe_dir, 'conan_req_version', None)

def get_conan_vars(recipe_dir):
    org_name = os.getenv("CONAN_ORGANIZATION_NAME", DEFAULT_ORGANIZATION_NAME)
    login_username = os.getenv("CONAN_LOGIN_USERNAME", DEFAULT_LOGIN_USERNAME)
    username = os.getenv("CONAN_USERNAME", get_user(recipe_dir))
    channel = os.getenv("CONAN_CHANNEL", get_channel(recipe_dir))
    version = os.getenv("CONAN_VERSION", get_version(recipe_dir))
    return org_name, login_username, username, channel, version

def get_value_from_recipe(recipe_dir, search_string, recipe_name="conanfile.py"):
    # recipe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', recipe_name)
    recipe_path = os.path.join(recipe_dir, recipe_name)
    with open(recipe_path, "r") as conanfile:
        contents = conanfile.read()
        result = re.search(search_string, contents)
    return result

def get_name_from_recipe(recipe_dir):
    return get_value_from_recipe(recipe_dir, r'''name\s*=\s*["'](\S*)["']''').groups()[0]

def get_user_repository(org_name, repository_name):
    # https://api.bintray.com/conan/k-nuth/kth
    # return "https://api.bintray.com/conan/{0}/{1}".format(org_name.lower(), repository_name)
    return "https://knuth.jfrog.io/artifactory/api/conan/knuth"

def get_conan_upload(org_name):
    repository_name = get_repository()
    return os.getenv("CONAN_UPLOAD", get_user_repository(org_name, repository_name))

def get_conan_upload_for_remote(org_name):
    repository_name = get_repository()
    return get_user_repository(org_name, repository_name)

def get_conan_remotes(org_name):
    # While redundant, this moves upload remote to position 0.
    # remotes = [get_conan_upload_for_remote(org_name),
    #           'https://knuth.jfrog.io/artifactory/api/conan/knuth',
    #           'https://taocpp.jfrog.io/artifactory/api/conan/tao',]

    remotes = ['https://center.conan.io',
               get_conan_upload_for_remote(org_name),
               'https://taocpp.jfrog.io/artifactory/api/conan/tao']

    # # Add bincrafters repository for other users, e.g. if the package would
    # # require other packages from the bincrafters repo.
    # bincrafters_user = "bincrafters"
    # if username != bincrafters_user:
    #     remotes.append(get_conan_upload(bincrafters_user))
    return remotes

def get_os():
    return platform.system().replace("Darwin", "Macos")

def get_archs():
    return ["x86_64"]

def get_builder(recipe_dir, args=None):
    name = get_name_from_recipe(recipe_dir)
    org_name, login_username, username, channel, version = get_conan_vars(recipe_dir)
    reference = "{0}/{1}".format(name, version)
    upload = get_conan_upload(org_name)
    remotes = os.getenv("CONAN_REMOTES", get_conan_remotes(org_name))

    os.getenv("CONAN_STABLE_BRANCH_PATTERN", "stable/*")

    archs = get_archs()

    builder = get_conan_packager().ConanMultiPackager(
        # args=args,    # Removed on https://github.com/conan-io/conan-package-tools/pull/269
        # pip_install=["kthbuild==0.17.0", "conan-promote==0.1.2"]
        # pip_install=["--install-option='--no-remotes=True' kthbuild"],
        pip_install=["kthbuild"],
        username=username,
        login_username=login_username,
        channel=channel,
        reference=reference,
        upload=upload,
        remotes=remotes,
        archs=archs,
        # upload_only_when_stable=upload_when_stable,
        # stable_branch_pattern=stable_branch_pattern
        )

    return builder, name

# --------------------------------------------

def handle_microarchs(opt_name, microarchs, filtered_builds, settings, options, env_vars, build_requires):
    microarchs = list(set(microarchs))

    for ma in microarchs:
        opts_copy = copy.deepcopy(options)
        opts_copy[opt_name] = ma
        filtered_builds.append([settings, opts_copy, env_vars, build_requires])

def get_base_march_ids():
    # return ['4fZKi37a595hP']        # haswell
    return [level3_marchid()]

def level3_marchid():
    exts = level3_on()
    return encode_extensions(exts)

def level2_marchid():
    exts = level2_on()
    return encode_extensions(exts)

def level1_marchid():
    exts = level1_on()
    return encode_extensions(exts)

def level0_marchid():
    exts = level0_on()
    return encode_extensions(exts)

def filter_marchs_tests(name, builds, test_options, march_opt=None):
    if march_opt is None:
        # march_opt = "%s:microarchitecture" % name
        march_opt = "%s:march_id" % name

    for b in builds:
        options = b[1]
        if options[march_opt] != "x86-64":
            for to in test_options:
                options[to] = "False"

# usage:
# conan install package -o march_id=? -o march_strategy=quick (default)
# conan install package -o march_id=? -o march_strategy=optimized

# -o march_strategy=download_if_possible (default)
# -o march_strategy=optimized
# -o march_strategy=download_or_fail

# -o march_from=compiler (default)
# -o march_from=cpu
# -o march_from=both

def march_conan_manip(conanobj):
    if conanobj.settings.arch != "x86_64":
        return (None, None, None)

    if conanobj.options.get_safe("march_id") is None:
        return (None, None, None)

    if conanobj.options.get_safe("march_strategy") is None:
        return (None, None, None)

    conanobj.march_from_cpuid = True
    march_id = None
    march_names = None
    march_flags = None

    if conanobj.options.march_id == "_DUMMY_":
        march_kth_defs = None

        conanobj.march_data = get_all_data(str(conanobj.settings.os),
                                        str(conanobj.settings.compiler),
                                        float(str(conanobj.settings.compiler.version)))

        if conanobj.options.march_strategy == "optimized":
            conanobj.output.info(f"Using an instruction set/extensions optimized for your platform (CPU, OS, Compiler)")

            level3_exts = conanobj.march_data['level3_exts']
            exts = conanobj.march_data['comp_exts']

            if is_superset_of(exts, level3_exts):
                exts_diff = set_diff(exts, level3_exts)
                exts_names = extensions_to_names(exts_diff)
                exts_str = ", ".join(exts_names)
                conanobj.output.info(f"Your platform is a is better than the reference platform (x86-64-v3) since it has the following set of instructions that the reference does not have: {exts_str}.")
            else:
                exts_diff = set_diff(level3_exts, exts)
                exts_names = extensions_to_names(exts_diff)
                exts_str = ", ".join(exts_names)
                conanobj.output.warn(f"Your platform is not compatible the reference platform (x86-64-v3).\nThe following extensions are not supported by your platform: {exts_str}.")

            march_id = conanobj.march_data['comp_marchid']
            march_names = conanobj.march_data['comp_names']
            march_flags = conanobj.march_data['comp_flags']
        elif conanobj.options.march_strategy == "download_if_possible":
            march_id = conanobj.march_data['comp_marchid']
            march_names = conanobj.march_data['comp_names']
            march_flags = conanobj.march_data['comp_flags']
            exts = conanobj.march_data['comp_exts']
            level3_exts = conanobj.march_data['level3_exts']

            if is_superset_of(exts, level3_exts):
                march_id = conanobj.march_data['level3_marchid']
                march_names = conanobj.march_data['level3_names']
                march_flags = conanobj.march_data['level3_flags']

                exts_diff = set_diff(exts, level3_exts)
                exts_names = extensions_to_names(exts_diff)
                exts_str = ", ".join(exts_names)
                conanobj.output.info(f"Your platform is a is better than the reference platform (x86-64-v3) since it has the following set of instructions that the reference does not have: {exts_str}.")
                conanobj.output.info(f"Even though your platform is better than the reference platform, the package you are downloading was compiled for the reference platform (it is less optimized).\nIf you want to take advantage of the full power of your platform, you must execute the conan command using -o march_strategy=optimized.")

            else:
                exts_diff = set_diff(level3_exts, exts)
                exts_names = extensions_to_names(exts_diff)
                exts_str = ", ".join(exts_names)
                conanobj.output.warn(f"Your platform is not compatible the reference platform (x86-64-v3).\nThe following extensions are not supported by your platform: {exts_str}.")

        elif conanobj.options.march_strategy == "download_or_fail":
            # conanobj.output.info(f"download_or_fail {conanobj.march_data}")

            exts = conanobj.march_data['comp_exts']
            level3_exts = conanobj.march_data['level3_exts']

            if not is_superset_of(exts, level3_exts):
                return (None, None, None)

            exts_diff = set_diff(exts, level3_exts)
            exts_names = extensions_to_names(exts_diff)
            exts_str = ", ".join(exts_names)
            conanobj.output.info(f"Your platform is a is better than the reference platform (x86-64-v3) since it has the following set of instructions that the reference does not have: {exts_str}.")
            conanobj.output.info(f"Even though your platform is better than the reference platform, the package you are downloading was compiled for the reference platform (it is less optimized).\nIf you want to take advantage of the full power of your platform, you must execute the conan command using -o march_strategy=optimized.")

            march_id = conanobj.march_data['level3_marchid']
            march_names = conanobj.march_data['level3_names']
            march_flags = conanobj.march_data['level3_flags']

        conanobj.options.march_id = march_id
    else:
        march_id = str(conanobj.options.march_id)
        conanobj.march_from_cpuid = False

        if march_id == "x86-64-v3":
            march_id = level3_marchid()
            conanobj.output.info(f"x86-64-v3 microarchitecture ID is translated to {march_id}")
        elif march_id == "x86-64-v2":
            march_id = level2_marchid()
            conanobj.output.info(f"x86-64-v2 microarchitecture ID is translated to {march_id}")
        elif march_id == "x86-64-v1":
            march_id = level1_marchid()
            conanobj.output.info(f"x86-64-v1 microarchitecture ID is translated to {march_id}")
        elif march_id == "x86-64-v0":
            march_id = level0_marchid()
            conanobj.output.info(f"x86-64-v0 microarchitecture ID is translated to {march_id}")
        elif march_id == "x86-64":
            march_id = level0_marchid()
            conanobj.output.info(f"x86-64 microarchitecture ID is translated to {march_id}")

        conanobj.march_data = get_all_data_from_marchid(
                                        march_id,
                                        str(conanobj.settings.os),
                                        str(conanobj.settings.compiler),
                                        float(str(conanobj.settings.compiler.version)))

        march_names = conanobj.march_data['user_names']
        march_flags = conanobj.march_data['user_flags']
        march_kth_defs = conanobj.march_data['user_kth_defs']

        #TODO(fernando): marchid errors?
        #TODO(fernando): march_strategy ??


        # if conanobj.options.march_strategy == "optimized":
        #     march_names = conanobj.march_data['comp_names']
        #     march_flags = conanobj.march_data['comp_flags']
        # elif conanobj.options.march_strategy == "download_if_possible":

    if conanobj.march_from_cpuid:
        conanobj.output.info(f"Detected microarchitecture ID: {march_id}")
    else:
        conanobj.output.info(f"User-defined microarchitecture ID: {march_id}")

    return (march_id, march_names, march_flags, march_kth_defs)

def pass_march_to_compiler(conanobj, cmake):
    if conanobj.options.get_safe("march_id") is None:
        return

    march_id = str(conanobj.options.march_id)
    flags = get_compiler_flags_arch_id(march_id,
                            str(conanobj.settings.os),
                            str(conanobj.settings.compiler),
                            float(str(conanobj.settings.compiler.version)))

    conanobj.output.info("Compiler flags: %s" % flags)
    # conanobj.output.info("Prev CONAN_CXX_FLAGS: %s" % cmake.definitions.get("CONAN_CXX_FLAGS", ""))
    # conanobj.output.info("Prev CONAN_C_FLAGS: %s" % cmake.definitions.get("CONAN_C_FLAGS", ""))

    cmake.definitions["CONAN_CXX_FLAGS"] = cmake.definitions.get("CONAN_CXX_FLAGS", "") + " " + flags
    cmake.definitions["CONAN_C_FLAGS"] = cmake.definitions.get("CONAN_C_FLAGS", "") + " " + flags

    if conanobj.march_names_full_str is not None:
        if conanobj.settings.compiler == "Visual Studio":
            cmake.definitions["CONAN_CXX_FLAGS"] = cmake.definitions.get("CONAN_CXX_FLAGS", "") + " /DKTH_MARCH_NAMES_FULL_STR=\\\"%s\\\"" % conanobj.march_names_full_str
            cmake.definitions["CONAN_C_FLAGS"] = cmake.definitions.get("CONAN_C_FLAGS", "") + " /DKTH_MARCH_NAMES_FULL_STR=\\\"%s\\\"" % conanobj.march_names_full_str
        else:
            cmake.definitions["CONAN_CXX_FLAGS"] = cmake.definitions.get("CONAN_CXX_FLAGS", "") + " -DKTH_MARCH_NAMES_FULL_STR=\\\"%s\\\"" % conanobj.march_names_full_str
            cmake.definitions["CONAN_C_FLAGS"] = cmake.definitions.get("CONAN_C_FLAGS", "") + " -DKTH_MARCH_NAMES_FULL_STR=\\\"%s\\\"" % conanobj.march_names_full_str

def get_conan_get(package, remote=None, default=None):
    try:
        if remote is None:
            params = ["conan", "get", package]
        else:
            params = ["conan", "get", package, "-r", remote]

        res = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = res.communicate()
        if output:
            if res.returncode == 0:
                return output.decode("utf-8")
        return default
    except OSError: # as e:
        return default
    except:
        return default

def get_recipe_dir():
    recipe_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.normpath(recipe_dir + os.sep + os.pardir)

def get_conan_requirements_path():
    return os.path.normpath(get_recipe_dir() + os.sep + 'conan_requirements')

def get_requirements_from_file():
    conan_requirements = get_conan_requirements_path()
    if os.path.exists(conan_requirements):
        with open(conan_requirements, 'r') as f:
            return [line.rstrip('\n') for line in f]
    return []

class KnuthConanFile(ConanFile):
    @property
    def conan_req_version(self):
        return get_conan_req_version(self.recipe_dir())

    def config_options(self):
        ConanFile.config_options(self)

        if self.settings.arch != "x86_64":
            self.output.info("march_id is disabled for architectures other than x86_64, your architecture: %s" % (self.settings.arch,))
            self.options.remove("march_id")
            self.options.remove("march_strategy")

        if self.settings.compiler == "Visual Studio":
            self.options.remove("fPIC")
            if self.is_shared:
                self.options.remove("shared")

    # def _warn_missing_options(self):
    #     if self.settings.arch == "x86_64" and self.options.get_safe("march_id") is None:
    #         self.output.warn("**** The recipe does not implement the march_id option. ****")

    def validate(self):
        # self.output.info(f"validate() self.march_data: {self.march_data}")
        # self.output.info(f"validate() self.march_from_cpuid: {self.march_from_cpuid}")

        # ConanFile.validate(self)

        if self.conan_req_version != None and Version(conan_version) < Version(self.conan_req_version):
            raise ConanInvalidConfiguration("Conan version should be greater or equal than %s. Detected: %s." % (self.conan_req_version, conan_version))

        v = Version(str(self.settings.compiler.version))
        if self.settings.compiler == "apple-clang" and v < "13":
            raise ConanInvalidConfiguration(f"apple-clang {v} not supported, you need to install apple-clang >= 13.")

        if self.settings.compiler == "clang" and v < "7":
            raise ConanInvalidConfiguration(f"Clang {v} not supported, you need to install Clang >= 7.")

        if self.settings.compiler == "gcc" and v < "5":
            raise ConanInvalidConfiguration(f"GCC {v} not supported, you need to install GCC >= 5.")

        #TODO(fernando): proper versions of Visual Studio and MSVC
        if self.settings.compiler == "Visual Studio" and v < "16":
            raise ConanInvalidConfiguration(f"Visual Studio (MSVC) {v} not supported, you need to install Visual Studio >= 16.")

        if self.settings.os == "Linux" and self.settings.compiler == "gcc" and self.settings.compiler.libcxx == "libstdc++":
            raise ConanInvalidConfiguration("We just support GCC C++11ABI.\n**** Please run `conan profile update settings.compiler.libcxx=libstdc++11 default`")

        if self.settings.arch == "x86_64":
            if self.options.get_safe("march_id") is None:
                raise ConanInvalidConfiguration("The recipe does not implement the march_id option.")

            if self.options.get_safe("march_strategy") is None:
                raise ConanInvalidConfiguration("The recipe does not implement the march_strategy option.")

            if self.march_from_cpuid:
                if self.options.march_strategy == "download_or_fail":
                    exts = self.march_data['comp_exts']
                    level3_exts = self.march_data['level3_exts']
                    if not is_superset_of(exts, level3_exts):
                        exts_diff = set_diff(level3_exts, exts)
                        exts_names = extensions_to_names(exts_diff)
                        exts_str = ", ".join(exts_names)
                        raise ConanInvalidConfiguration(f"The detected microarchitecture of your platform is not compatible with x86-64-v3 (Check https://en.wikipedia.org/wiki/X86-64#Microarchitecture_levels).\nThe following extensions are not supported by your platform: {exts_str}.\nThis error is generated because you chose -o march_strategy=download_or_fail.")
            else:
                if not self.march_data['user_marchid_valid']:
                    raise ConanInvalidConfiguration(f"{self.options.get_safe('march_id')} is not a valid microarchitecture id (march_id option).")

                exts = self.march_data['user_exts']
                exts_filtered = self.march_data['user_exts_filtered']
                if not is_superset_of(exts_filtered, exts):
                    exts_diff = set_diff(exts, exts_filtered)
                    exts_names = extensions_to_names(exts_diff)
                    exts_str = ", ".join(exts_names)
                    raise ConanInvalidConfiguration(f"{self.options.get_safe('march_id')} is not compatible with your compiler.\nThe following extensions are not supported by your compiler: {exts_str}.")


    def configure(self, pure_c=False):
        # if self.conan_req_version != None and Version(conan_version) < Version(self.conan_req_version):
        #     raise Exception ("Conan version should be greater or equal than %s. Detected: %s." % (self.conan_req_version, conan_version))

        ConanFile.configure(self)

        if pure_c:
            del self.settings.compiler.libcxx               #Pure-C Library

        if self.options.get_safe("currency") is not None:
            self.options["*"].currency = self.options.currency
            self.output.info("Compiling for currency: %s" % (self.options.currency,))

        if self.options.get_safe("db") is not None:
            self.options["*"].db = self.options.db
            self.output.info("Compiling for DB: %s" % (self.options.db,))

        # self._warn_missing_options()

        if self.settings.arch == "x86_64":
            (march_id, march_names, march_flags, march_kth_defs) = march_conan_manip(self)
            if march_names is not None:
                self.march_names_full_str = ', '.join(march_names)
                self.output.info(f"The package is being compiled for a platform that supports: {self.march_names_full_str}")

            self.options["*"].march_id = march_id
            self.options["*"].march_strategy = self.options.get_safe("march_strategy")

            if self.options.get_safe("march_id") is not None:
                self.options.march_id = march_id

            #TODO(fernando)
            # if self.options.get_safe("march_id") is not None:
            #     self.output.info("Building microarchitecture ID: %s" % march_id)
            #     exts = decode_extensions(march_id)
            #     exts_names = extensions_to_names(exts)
            #     self.output.info(", ".join(exts_names))


    def package_id(self):
        ConanFile.package_id(self)

        v = Version(str(self.settings.compiler.version))
        # if self.settings.compiler == "gcc" and self.settings.compiler.version == "4.9":

        # self.output.info(f"self.settings.compiler: {self.settings.compiler}")
        # self.output.info(f"v:                      {v}")

        # # if self.settings.compiler == "gcc" and (v >= "5" and v <= "12"):
        # #     for version in ("5", "6", "7", "8", "9", "10", "11", "12"):
        # #         self.output.info(f"version:                 {version}")
        # #         self.output.info(f"version != v:            {version != v}")
        # #         if version != v:
        # #             compatible_pkg = self.info.clone()
        # #             compatible_pkg.settings.compiler.version = version
        # #             self.compatible_packages.append(compatible_pkg)

        # if self.settings.compiler == "gcc" and (v >= "11" and v <= "12"):
        #     for version in ("11", "12"):
        #         self.output.info(f"version:                 {version}")
        #         self.output.info(f"version != v:            {version != v}")
        #         if version != v:
        #             compatible_pkg = self.info.clone()
        #             compatible_pkg.settings.compiler.version = version
        #             self.compatible_packages.append(compatible_pkg)

        # if self.settings.compiler == "clang" and (v >= "7" and v <= "14"):
        #     for version in ("7", "8", "9", "10", "11", "12", "13", "14"):
        #         compatible_pkg = self.info.clone()
        #         compatible_pkg.settings.compiler.version = version
        #         self.compatible_packages.append(compatible_pkg)

        # if self.settings.compiler == "apple-clang" and (v >= "13" and v <= "13"):
        #     for version in ("13"):
        #         compatible_pkg = self.info.clone()
        #         compatible_pkg.settings.compiler.version = version
        #         self.compatible_packages.append(compatible_pkg)

        # if self.settings.compiler == "gcc" and (v >= "5" and v <= "12"):
        #     self.info.settings.compiler.version = "GCC [5, 12]"

        if self.settings.compiler == "gcc" and (v >= "11"):
            self.info.settings.compiler.version = "GCC >= 11"
        else:
            self.info.settings.compiler.version = "GCC < 11"

        if self.settings.compiler == "clang" and (v >= "7" and v <= "14"):
            self.info.settings.compiler.version = "Clang [7, 14]"

        if self.settings.compiler == "apple-clang" and (v >= "13" and v <= "13"):
            self.info.settings.compiler.version = "apple-clang [13, 13]"

        # self.output.info(f"compatible_packages: {self.compatible_packages}")

        #TODO(fernando): MSVC

        if self.options.get_safe("verbose") is not None:
            self.info.options.verbose = "ANY"

        if self.options.get_safe("cxxflags") is not None:
            self.info.options.cxxflags = "ANY"

        if self.options.get_safe("cflags") is not None:
            self.info.options.cflags = "ANY"

        if self.options.get_safe("tests") is not None:
            self.info.options.tests = "ANY"

        if self.options.get_safe("tools") is not None:
            self.info.options.tools = "ANY"

        if self.options.get_safe("examples") is not None:
            self.info.options.examples = "ANY"

        if self.options.get_safe("cmake_export_compile_commands") is not None:
            self.info.options.cmake_export_compile_commands = "ANY"

        if self.options.get_safe("march_strategy") is not None:
            self.info.options.march_strategy = "ANY"

    def _cmake_database(self, cmake):
        if self.options.get_safe("db") is None:
            return

        if self.options.db == "legacy":
            cmake.definitions["DB_TRANSACTION_UNCONFIRMED"] = option_on_off(False)
            cmake.definitions["DB_SPENDS"] = option_on_off(False)
            cmake.definitions["DB_HISTORY"] = option_on_off(False)
            cmake.definitions["DB_STEALTH"] = option_on_off(False)
            cmake.definitions["DB_UNSPENT_LEGACY"] = option_on_off(True)
            cmake.definitions["DB_LEGACY"] = option_on_off(True)
            cmake.definitions["DB_NEW"] = option_on_off(False)
            cmake.definitions["DB_NEW_BLOCKS"] = option_on_off(False)
            cmake.definitions["DB_NEW_FULL"] = option_on_off(False)
        elif self.options.db == "legacy_full":
            cmake.definitions["DB_TRANSACTION_UNCONFIRMED"] = option_on_off(True)
            cmake.definitions["DB_SPENDS"] = option_on_off(True)
            cmake.definitions["DB_HISTORY"] = option_on_off(True)
            cmake.definitions["DB_STEALTH"] = option_on_off(True)
            cmake.definitions["DB_UNSPENT_LEGACY"] = option_on_off(True)
            cmake.definitions["DB_LEGACY"] = option_on_off(True)
            cmake.definitions["DB_NEW"] = option_on_off(False)
            cmake.definitions["DB_NEW_BLOCKS"] = option_on_off(False)
            cmake.definitions["DB_NEW_FULL"] = option_on_off(False)
        elif self.options.db == "pruned":
            cmake.definitions["DB_TRANSACTION_UNCONFIRMED"] = option_on_off(False)
            cmake.definitions["DB_SPENDS"] = option_on_off(False)
            cmake.definitions["DB_HISTORY"] = option_on_off(False)
            cmake.definitions["DB_STEALTH"] = option_on_off(False)
            cmake.definitions["DB_UNSPENT_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_NEW"] = option_on_off(True)
            cmake.definitions["DB_NEW_BLOCKS"] = option_on_off(False)
            cmake.definitions["DB_NEW_FULL"] = option_on_off(False)
        elif self.options.db == "default":
            cmake.definitions["DB_TRANSACTION_UNCONFIRMED"] = option_on_off(False)
            cmake.definitions["DB_SPENDS"] = option_on_off(False)
            cmake.definitions["DB_HISTORY"] = option_on_off(False)
            cmake.definitions["DB_STEALTH"] = option_on_off(False)
            cmake.definitions["DB_UNSPENT_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_NEW"] = option_on_off(True)
            cmake.definitions["DB_NEW_BLOCKS"] = option_on_off(True)
            cmake.definitions["DB_NEW_FULL"] = option_on_off(False)
        elif self.options.db == "full":
            cmake.definitions["DB_TRANSACTION_UNCONFIRMED"] = option_on_off(False)
            cmake.definitions["DB_SPENDS"] = option_on_off(False)
            cmake.definitions["DB_HISTORY"] = option_on_off(False)
            cmake.definitions["DB_STEALTH"] = option_on_off(False)
            cmake.definitions["DB_UNSPENT_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_NEW"] = option_on_off(True)
            cmake.definitions["DB_NEW_BLOCKS"] = option_on_off(False)
            cmake.definitions["DB_NEW_FULL"] = option_on_off(True)

    def cmake_basis(self, pure_c=False):
        cmake = CMake(self)
        cmake.definitions["USE_CONAN"] = option_on_off(True)
        cmake.definitions["NO_CONAN_AT_ALL"] = option_on_off(False)
        cmake.verbose = self.options.verbose
        cmake.definitions["ENABLE_SHARED"] = option_on_off(self.is_shared)
        cmake.definitions["ENABLE_POSITION_INDEPENDENT_CODE"] = option_on_off(self.fPIC_enabled)

        if self.options.get_safe("tests") is not None:
            cmake.definitions["WITH_TESTS"] = option_on_off(self.options.tests)
            cmake.definitions["WITH_TESTS_NEW"] = option_on_off(self.options.tests)

        if self.options.get_safe("examples") is not None:
            cmake.definitions["WITH_EXAMPLES"] = option_on_off(self.options.examples)

        if self.options.get_safe("tools") is not None:
            cmake.definitions["WITH_TOOLS"] = option_on_off(self.options.tools)

        if self.options.get_safe("cxxflags") is not None and self.options.cxxflags != "_DUMMY_":
            cmake.definitions["CONAN_CXX_FLAGS"] = cmake.definitions.get("CONAN_CXX_FLAGS", "") + " " + str(self.options.cxxflags)
        if self.options.get_safe("cflags") is not None and self.options.cflags != "_DUMMY_":
            cmake.definitions["CONAN_C_FLAGS"] = cmake.definitions.get("CONAN_C_FLAGS", "") + " " + str(self.options.cflags)

        if self.settings.compiler != "Visual Studio":
            # cmake.definitions["CONAN_CXX_FLAGS"] += " -Wno-deprecated-declarations"
            cmake.definitions["CONAN_CXX_FLAGS"] = cmake.definitions.get("CONAN_CXX_FLAGS", "") + " -Wno-deprecated-declarations"
        if self.settings.compiler == "Visual Studio":
            cmake.definitions["CONAN_CXX_FLAGS"] = cmake.definitions.get("CONAN_CXX_FLAGS", "") + " /DBOOST_CONFIG_SUPPRESS_OUTDATED_MESSAGE"

        if self.options.get_safe("march_id") is not None:
            cmake.definitions["MARCH_ID"] = self.options.march_id

        cmake.definitions["KTH_PROJECT_VERSION"] = self.version

        if self.options.get_safe("currency") is not None:
            cmake.definitions["CURRENCY"] = self.options.currency

        self._cmake_database(cmake)

        if self.options.get_safe("cmake_export_compile_commands") is not None and self.options.cmake_export_compile_commands:
            cmake.definitions["CMAKE_EXPORT_COMPILE_COMMANDS"] = option_on_off(self.options.cmake_export_compile_commands)

        if not pure_c:
            if self.settings.compiler == "gcc":
                if float(str(self.settings.compiler.version)) >= 5:
                    cmake.definitions["NOT_USE_CPP11_ABI"] = option_on_off(False)
                else:
                    cmake.definitions["NOT_USE_CPP11_ABI"] = option_on_off(True)
            elif self.settings.compiler == "clang":
                if str(self.settings.compiler.libcxx) == "libstdc++" or str(self.settings.compiler.libcxx) == "libstdc++11":
                    cmake.definitions["NOT_USE_CPP11_ABI"] = option_on_off(False)

        pass_march_to_compiler(self, cmake)
        # self.output.info("CONAN_CXX_FLAGS: %s" % (cmake.definitions["CONAN_CXX_FLAGS"], ))
        # self.output.info("cmake.command_line: %s" % (cmake.command_line, ))
        return cmake


    def add_reqs(self, reqs):
        for r in reqs:
            self.requires(r % (self.user, self.channel))

    def knuth_requires(self, default_reqs):
        file_reqs = get_requirements_from_file()
        # print(file_reqs)

        if len(file_reqs) != 0:
            self.add_reqs(file_reqs)
        else:
            self.add_reqs(default_reqs)

    @property
    def msvc_mt_build(self):
        # return "MT" in str(self.settings.compiler.runtime)
        return "MT" in str(self.settings.get_safe("compiler.runtime"))

    @property
    def fPIC_enabled(self):
        if self.options.get_safe("fPIC") is None:
            return False

        if self.settings.compiler == "Visual Studio":
            return False

        return self.options.fPIC

    @property
    def is_shared(self):
        if self.options.get_safe("shared") is None:
            return False

        if self.options.shared and self.msvc_mt_build:
            return False
        else:
            return self.options.shared

    @property
    def channel(self):
        try:
            return super(KnuthConanFile, self).channel
        except ConanException:
            return get_channel(self.recipe_dir())

    @property
    def user(self):
        try:
            return super(KnuthConanFile, self).user
        except ConanException:
            return get_user(self.recipe_dir())


# def main():
#     cf = KnuthConanFile()
#     cf.config_options()

# if __name__ == "__main__":
#     main()