from setuptools import find_packages, setup

setup(
    name = 'ouobypass',
    version = '0.0.1',
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
            'ouobypass = ouobypass.ouo_bypass:ouo'
        ]
    }
)