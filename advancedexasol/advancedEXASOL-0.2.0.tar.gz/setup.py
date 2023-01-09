from setuptools import setup

setup(
    name='advancedEXASOL',
    version='0.2.0',
    description="advancedEXASOL is a Python library that extends pyexasol's functionality.",
    author='Damien Frigewski',
    author_email='dfrigewski@gmail.com',
    url='https://github.com/DamienDrash/advancedEXASOL',
    packages=['advancedEXASOL'],
    install_requires=['pyexasol', 'dask', 'pandas', 'xlwt'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
)
