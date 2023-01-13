from setuptools import setup, find_packages

setup(
    name='chesschecker',
    version='420',
    author='fetishized',
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
            'chesschecker = chesschecker.main:main'
        ],
    },
)