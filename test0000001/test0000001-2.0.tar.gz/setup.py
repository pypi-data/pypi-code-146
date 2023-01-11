from setuptools import setup, find_packages

setup(
    name="test0000001",
    version="2.0",
    package_dir={'test0000001': 'test0000001'},
    packages=find_packages(),
    install_requires=[
        'pyrebase',
        'logger',
        'logging',
        'uuid',
        'python-dotenv',
        'python-datetime'
    ],
    entry_points={
        'console_scripts': [
            'test0000001 = test0000001.steps:run_steps'
        ]
    }
)
