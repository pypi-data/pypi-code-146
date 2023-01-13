import setuptools
import version

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='ml-cli-azureml-pipeline',
    version=version.VERSION,
    packages=setuptools.find_packages(exclude=["tests", "tests.*"], where='src'),
    package_dir={'': 'src'},
    install_requires=requirements,
    author="Axa_france",
    author_email="guillaume.chervet@axa.fr",
    url='https://github.com/AxaGuilDEv/ml-cli-azureml-pipeline',
    description="ML-Cli run in an azureML Pipeline",
    long_description="Run our ML integration test automaticaly on production environment so we can compute : prediction quality, response time, infrastructure cost",
    platforms='POSIX',
    classifiers=["Programming Language :: Python :: 3 :: Only",
                 "Programming Language :: Python :: 3.8",
                 "Topic :: Scientific/Engineering :: Information Analysis",
                 ]
)
