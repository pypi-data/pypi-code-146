import versioneer
from setuptools import setup, find_namespace_packages

with open('requirements.txt') as f:
    REQUIREMENTS = f.readlines()

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name='drb-driver-discodata',
    packages=find_namespace_packages(include=['drb.*']),
    description='DRB DISCODATA Driver',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='GAEL Systems',
    author_email='drb-python@gael.fr',
    url='https://gitlab.com/drb-python/impl/discodata',
    install_requires=REQUIREMENTS,
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.8',
    entry_points={
        'drb.driver': 'discodata = drb.drivers.discodata:DiscodataFactory',
        'drb.topic': 'discodata = drb.topics.discodata'
    },
    package_data={
        'drb.topics.discodata': ['cortex.yml']
    },
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    data_files=[('.', ['requirements.txt'])],
    project_urls={
        'Documentation': 'https://drb-python.gitlab.io/impl/discodata',
        'Source': 'https://gitlab.com/drb-python/impl/discodata',
    }
)
