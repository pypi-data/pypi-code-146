from setuptools import setup

with open('README.md') as readme:
    README = readme.read()

with open('requirements.txt') as requirements_txt:
    requirements = requirements_txt.read().strip().splitlines()

setup(
    name='drf-extra-utils',
    version='1.0.1',
    license='MIT License',
    author='Gabriel Lustosa',
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    packages=['drf_extra_utils', 'drf_extra_utils.annotations', 'drf_extra_utils.related_object'],
    author_email='lustosaki2@gmail.com',
    description='Utils for django rest',
    python_requires=">=3.8",
)
