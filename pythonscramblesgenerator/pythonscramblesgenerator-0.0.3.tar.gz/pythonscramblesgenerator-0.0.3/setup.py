from setuptools import setup, find_packages

setup(
    name='pythonscramblesgenerator',
    version='0.0.3',
    author='BadSch00lBoy',
    author_email='artiomroshkoff@gmail.com',
    packages=find_packages("random"),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'generatorfile = generatorfile:generate_scramble'
        ]
    }
)