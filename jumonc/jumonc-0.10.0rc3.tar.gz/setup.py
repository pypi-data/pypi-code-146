import pathlib
from setuptools import setup

from jumonc._version import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="jumonc",
    version=__version__,
    description="Jülich Monitoring and Control",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.jsc.fz-juelich.de/coec/jumonc",
    author="Christian Witzler",
    author_email="c.witzler@fz-juelich.de",
    license="BSD 3-Clause License",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["jumonc"],
    extras_require={
        "PAPI": ["python-papi"],
        "NVLM": ["pynvml"],
        "GPU": ["pynvml"],
        "psutil": ["psutil"],
        "SSL": ["pyopenssl"],
        "Full": ["python-papi", "pynvml", "psutil", "pyopenssl"],
        "Devel": ["python-papi", "pynvml", "psutil", "pyopenssl", "prospector", "bandit", "mypy", "pytest", "coverage", "sqlalchemy[mypy]"]
    },
    include_package_data=True,
    install_requires=["flask", "flask_login", "mpi4py", "Flask-SQLAlchemy", "pluggy", 'typing_extensions; python_version < "3.10"'],
    entry_points={
        "console_scripts": [
            "jumonc=jumonc.start:start_jumonc",
            "JuMonC=jumonc.start:start_jumonc"
        ]
    },
)
