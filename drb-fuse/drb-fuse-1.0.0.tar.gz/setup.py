import versioneer
from setuptools import find_namespace_packages, setup

with open('requirements.txt') as f:
    REQUIREMENTS = f.readlines()

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name='drb-fuse',
    packages=find_namespace_packages(include=['drb.*']),
    description='DRB fuse implementation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='GAEL Systems',
    author_email='drb-python@gael.fr',
    url='https://git.gael.fr/gael10/drb/drb-python/drb_python_fuse',
    install_requires=REQUIREMENTS,
    test_suite='tests',
    data_files=[('.', ['requirements.txt'])],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.8',
    use_scm_version=True,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    project_urls={
        'Documentation': 'http://drb-python.gitlab.io/fuse',
        'Source': 'https://gitlab.com/drb-python/fuse',
    }
)
