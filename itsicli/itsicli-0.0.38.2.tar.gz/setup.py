import setuptools

from itsicli import __version__


with open('README.md', 'r') as fh:
    long_description = fh.read()


with open('requirements.txt') as fh:
    requirements = [line.strip() for line in fh.readlines()
                    if line.strip() and not line.startswith('--')]

setuptools.setup(
    name='itsicli',
    version=__version__,
    author='Splunk, Inc.',
    description='The ITSI Command Line Interface (CLI)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    scripts=[
        'bin/itsi-content-pack'
    ],
    url='https://github.com/splunk/itsi-cli',
    packages=setuptools.find_packages(),
    package_data={
        'itsicli.content_packs': ['resources/*']
    },
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
