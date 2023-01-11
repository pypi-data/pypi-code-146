from setuptools import setup, find_packages

VERSION = '1.0.2'
DESCRIPTION = 'segy2seg2'
LONG_DESCRIPTION = 'A package to convert segy seismic file to seg2 (dat) file'

# Setting up
setup(
    name="segy2seg2",
    version=VERSION,
    author="Shanu Biswas",
    author_email="shanubiswas119@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["obspy"],
    keywords=['segy', 'seismic', 'seg2', 'segy to seg2 converter', 'segy to dat file converter', 'segy to dat file converter using python' ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)