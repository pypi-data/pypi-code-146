#!/usr/bin/env python3
import os

from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))


### replace this data with your plugin specific info
PLUGIN_TYPE = "ovos.ocp.extractor"
PLUGIN_NAME = 'ovos-ocp-files-plugin'
PLUGIN_PKG = PLUGIN_NAME.replace("-", "_")
PLUGIN_CLAZZ = "OCPFilesMetadataExtractor"
PLUGIN_CONFIGS = f"{PLUGIN_CLAZZ}Config"
###

PLUGIN_ENTRY_POINT = f'{PLUGIN_NAME} = {PLUGIN_PKG}.plugin:{PLUGIN_CLAZZ}'
CONFIG_ENTRY_POINT = f'{PLUGIN_NAME}.config = {PLUGIN_PKG}:{PLUGIN_CONFIGS}'


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


setup(
    name=PLUGIN_NAME,
    version="0.12.0",
    description='metadata extractor from audio files',
    url='https://github.com/OpenVoiceOS/ovos-ocp-files-plugin',
    author='thebigmunch',
    author_email='mail@thebigmunch.me',
    license='MIT',
    packages=[PLUGIN_PKG],
    install_requires=required("requirements.txt"),
    package_data={'': package_files(PLUGIN_PKG)},
    zip_safe=True,
    include_package_data=True,
    keywords='ovos ocp plugin',
    entry_points={PLUGIN_TYPE: PLUGIN_ENTRY_POINT,
                  f'{PLUGIN_TYPE}.config': CONFIG_ENTRY_POINT}
)
