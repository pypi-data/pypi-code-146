from setuptools import setup, find_packages

setup(
    name='submerger',
    version='1.0.0',
    description='',

    author='Andrii Valiukh',
    author_email='andr.you.ay@gmail.com',

    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[],
    extras_require={
        'dev': [
            'mypy',
            'pylint',
        ]
    },
    scripts=['bin/submerge'],
)
