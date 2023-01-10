from setuptools import setup, find_packages

setup(
    name="test0000001",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'test0000001 = steps:run_steps'
        ]
    }
)
