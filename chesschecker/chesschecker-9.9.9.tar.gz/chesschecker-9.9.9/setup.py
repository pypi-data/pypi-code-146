from setuptools import setup, find_packages

setup(
    name='chesschecker',
    author='fetishized',
    version='9.9.9',
    url='https://github.com/fetishized/chesschecker',
    license='wtfpl',
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorama',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'chesschecker = __main__:main',
        ],
    },
)