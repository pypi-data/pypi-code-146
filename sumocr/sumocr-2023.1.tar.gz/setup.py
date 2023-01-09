from setuptools import setup, find_packages

# read the README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='sumocr',
    version='2023.1',
    description='Python tool to interface with the SUMO traffic simulator',
    keywords='autonomous automated vehicles driving motion planning',
    url='https://commonroad.in.tum.de/sumo-interface',
    project_urls={
        'Documentation': 'https://commonroad.in.tum.de/sumo-interface',
        'Forum': 'https://commonroad.in.tum.de/forum/c/sumo-interface',
        'Source': 'https://gitlab.lrz.de/tum-cps/commonroad-sumo-interface',
    },
    author='Cyber-Physical Systems Group, Technical University of Munich',
    author_email='commonroad@lists.lrz.de',
    license="BSD License",
    packages=find_packages(exclude=['ci','dist','example_scripts','not_for_public_repo','sumocr/docs','tests']),
    install_requires=[
        'numpy>=1.13',
        'lxml>=4.2.2',
        'Pillow>=7.0.0',
        'commonroad-io>=2022.3',
        # docker_sumo
        'shapely>=1.7.0',
        'grpcio>=1.27.2',
        'docker>=4.2.0',
        'packaging>=20.3',
        'ffmpeg>=1.4',
        'matplotlib>=3.3.3',
        'ipython',
        'libsumo>=1.12.0'
    ],
    extras_require={
        'doc': [
            'sphinx>=1.3.6', 'graphviz>=0.3',
            'sphinx-autodoc-typehints>=1.3.0', 'sphinx_rtd_theme>=0.4.1',
            'sphinx-gallery>=0.2.0', 'ipython>=6.5.0'
        ],
        'tests': [
            'lxml>=4.2.5',
            'pytest>=3.8.0',
        ],
    },
    long_description_content_type='text/markdown',
    long_description=readme,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    python_requires='>=3.7',
    data_files=[('.', ['LICENSE.txt'])],
    include_package_data=True,
)
