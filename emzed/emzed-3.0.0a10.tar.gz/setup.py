# This file is part of emzed (https://emzed.ethz.ch), a software toolbox for analysing
# LCMS data with Python.
#
# Copyright (C) 2020 ETH Zurich, SIS ID.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys
from distutils.command.build_ext import build_ext as _build_ext

from setuptools import Extension, find_packages, setup

from setuptools.command.develop import develop
from setuptools.command.install import install


install_requires = [
    "dill",
    "IsoSpecPy==2.2.1",
    "numpy>=1.17",
    "openpyxl",
    "pyper==1.1.1",
    "requests",
    "scikit-learn",
    "xlrd",
    "xlwt",
    "xlwt",
    "importlib-resources>=1.1.0; python_version < '3.9'",
]

DOWNLOAD_URL = "https://sis.id.ethz.ch/_downloads"

if sys.platform == "win32":
    install_requires += ["pywin32", "matplotlib==3.3.0", "pandas!=1.3.1"]
else:
    install_requires += ["matplotlib", "pandas"]


class build_ext(_build_ext):
    """only require numpy when we build binary extension"""

    def run(self):
        # https://stackoverflow.com/questions/21605927/
        __builtins__.__NUMPY_SETUP__ = False
        import numpy

        self.include_dirs += [numpy.get_include()]
        _build_ext.run(self)


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        develop.run(self)
        os.system(f"{sys.executable} -c 'import emzed'")


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        os.system(f"{sys.executable} -c 'import emzed'")


ext_modules = [
    Extension(
        "emzed.optimized.formula_fit",
        [os.path.join("src", "emzed", "optimized", "formula_fit.c")],
    )
]

setup(
    name="emzed",
    version="3.0.0a10",
    description="",
    url="",
    author="Uwe Schmitt",
    author_email="uwe.schmitt@id.ethz.ch",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    cmdclass={
        "build_ext": build_ext,
        "install": PostInstallCommand,
        "develop": PostDevelopCommand,
    },
    ext_modules=ext_modules,
)
