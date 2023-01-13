from setuptools import setup, find_packages


VERSION = '0.0.3'
DESCRIPTION = 'A basic space api'
LONG_DESCRIPTION = 'A package that enables you to request data for astronauts, launchers and launches'

# Setting up
setup(
    name="rocket-space-stuff",
    version=VERSION,
    author="Miro Rava",
    author_email="<miro.rava.commercial@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'api', 'space'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)