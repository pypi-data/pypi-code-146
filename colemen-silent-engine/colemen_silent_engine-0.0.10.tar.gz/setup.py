from setuptools import setup, find_packages
import build_utils as _bu

VERSION = '0.0.10'
DESCRIPTION = 'colemen_silentEngine'
LONG_DESCRIPTION = 'colemen_silentEngine'

PY_MODULES = _bu.list_py_modules()
_bu.purge_dist()

# Setting up
setup(
    name="colemen_silent_engine",
    version=VERSION,
    author="Colemen Atwood",
    author_email="<atwoodcolemen@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    py_modules=['silent_engine'] + PY_MODULES,
    # add any additional packages that
    # need to be installed along with your package. Eg: 'caer'
    install_requires=[
        'colemen_utils',
    ],

    keywords=['python'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
