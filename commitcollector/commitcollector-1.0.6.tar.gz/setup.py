from setuptools import setup

setup(
    name='commitcollector',
    version='1.0.6',
    py_modules=['commitcollector'],
    entry_points={
        'console_scripts': [
            'commitcollector = commitcollector:main'
        ]
    })