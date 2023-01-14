from setuptools import setup

README_FILE = open('README.md', 'r').read()

setup(
    name='celestis',
    version='2.1',
    description='A simple backend framework built using python',
    long_description_content_type="text/markdown",
    long_description=README_FILE,
    author="Aryaan Hegde",
    author_email="aryhegde@gmail.com",
    packages=["celestis.controller", "celestis.view", "celestis.model"],
    package_dir={"celestis.controller": "controller", "celestis.view": "view", "celestis.model": "model"},
    py_modules=['celestis', 'command', 'create_files', 'error', 'render', 'requests', 'read_models', 'database', 'exceptions'],
    include_package_data=True,
    install_requires=['requests', 'click'],
    entry_points={
        'console_scripts': [
            'celestis=command:celestis',
        ],
    },
)