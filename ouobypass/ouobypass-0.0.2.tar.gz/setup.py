from setuptools import find_packages, setup

setup(
    name = 'ouobypass',
    version = '0.0.2',
    install_requires = [
        'beautifulsoup4',
        'selenium'
    ],
    package_dir = {
        '' : 'src'
    },
    packages=find_packages(where='src'),
    entry_points = {
        'console_scripts' : [
            'ouobypass = ouobypass.main:ouo',
            'zipertobypass = ouobypass.main:ziperto'
        ]
    }
)