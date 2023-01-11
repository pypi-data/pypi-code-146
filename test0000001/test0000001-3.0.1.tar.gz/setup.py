from setuptools import setup, find_packages

setup(
    name="test0000001",
    version="3.0.1",
    package_dir={'test0000001': 'test0000001'},
    packages=find_packages(),
    install_requires=[
        'pyrebase',
        'uuid',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'test0000001 = test0000001.steps:run_steps'
        ]
    }
)

