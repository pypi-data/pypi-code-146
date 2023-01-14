from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Basic package'
LONG_DESCRIPTION = 'A Basic package with more text'

# Setting up
setup(
    name="edgenerator",
    version=VERSION,
    author="SiebeLeDe ",
    author_email="<siebe.lekannegezegddeprez@student.uva.nl>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy>=1.23.4', 'matplotlib>=3.6.2'],
    keywords=['python', 'energy diagram', 'energy diagram generator'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
#        "Operating System :: Unix",
#       "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)