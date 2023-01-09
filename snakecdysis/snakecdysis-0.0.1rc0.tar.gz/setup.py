#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path
from setuptools import setup, find_packages
# add for remove error with pip install -e . with pyproject.toml
import site
import sys

site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

NAME = "snakecdysis"
GIT_URL = "https://forge.ird.fr/phim/sravel/snakecdysis"
CURRENT_PATH = Path(__file__).resolve().parent
VERSION = str(CURRENT_PATH.joinpath(f"{NAME}", "VERSION").open('r').readline().strip())

__doc__ = """Snakecdysis"""


def main():
    setup(
        # Project information
        name=NAME,
        version=VERSION,
        url=GIT_URL,
        project_urls={
            "Bug Tracker": f"{GIT_URL}/issues",
            "Documentation": f"https://{NAME}.readthedocs.io/en/latest/",
            "Source Code": GIT_URL
        },
        download_url=f"{GIT_URL}/archive/{VERSION}.tar.gz",
        author="""Ravel Sebastien (CIRAD)""",
        author_email="sebastien.ravel@cirad.fr",
        description=__doc__.replace("\n", ""),
        long_description=CURRENT_PATH.joinpath('README.rst').open("r", encoding='utf-8').read(),
        long_description_content_type='text/x-rst',
        license='GPLv3',

        # docs compilation utils
        command_options={
            'build_sphinx': {
                'project': ('setup.py', NAME),
                'version': ('setup.py', VERSION),
                'release': ('setup.py', VERSION),
                'source_dir': ('setup.py', CURRENT_PATH.joinpath("docs", "source").as_posix()),
                'build_dir': ('setup.py', CURRENT_PATH.joinpath("docs", "build").as_posix()),
            }},

        # Package information
        packages=find_packages(),
        include_package_data=True,
        # use_scm_version={
        #     "version_scheme": 'release-branch-semver',
        #     'local_scheme': "SemVer",
        #     'normalize': True,
        #     "root": ".",
        #     "relative_to": __file__,
        #     "fallback_version": VERSION,
        #     "write_to": f'{NAME}/_version.py',
        #     'tag_regex': r'^(?P<prefix>v)?(?P<version>[^\+]+)?$',
        # },
        use_scm_version=False,
        setup_requires=['setuptools_scm'],
        python_requires=">=3.8",
        install_requires=[
            'PyYAML',
            'snakemake',
            'tqdm',
            'click>=8.0.3',
            'cookiecutter',
            'docutils < 0.18',
            'python-gitlab'
        ],
        extras_require={
            'dev': ['sphinx_copybutton',
                    'sphinx_rtd_theme',
                    'sphinx_click',
                    'tox'],
        },
        entry_points={
            NAME: [f"{NAME} = __init__"],
            'console_scripts': [f"{NAME} = {NAME}.main:main"],
        },

        # Pypi information
        platforms=['unix', 'linux'],
        keywords=[
            'snakemake',
            'wrapper',
            'installation'
        ],
        classifiers=[
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            'License :: CeCILL-C Free Software License Agreement (CECILL-C)',
            'License :: Free for non-commercial use',
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Natural Language :: English',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
        ],
        options={
            'bdist_wheel': {'universal': True}
        },
        zip_safe=True,  # Don't install the lib as an .egg zipfile
    )


if __name__ == '__main__':
    main()
