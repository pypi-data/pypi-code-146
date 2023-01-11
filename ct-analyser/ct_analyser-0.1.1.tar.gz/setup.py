import setuptools

from ct_analyser import __version__, __author__

# Read contents of requirements.txt
with open('requirements.txt') as rq:
    req = []
    for line in rq.read().splitlines():
        if not line.startswith('#'):
            req.append(line)

# Read contents of README.md
with open('README.md') as rm:
    long_description = rm.read()

setuptools.setup(
    name='ct_analyser',
    version=__version__,
    author=__author__,

    license = 'The MIT License (MIT)',
    license_files = ('LICENSE',),
    description='A Python package for analysing CT scans',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages = setuptools.find_packages(),
    include_package_data = True,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent'],
    python_requires='>=3.8.8',
    install_requires=req,
)