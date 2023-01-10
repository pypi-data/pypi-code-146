from setuptools import setup

with open('README.md') as readme:
    README = readme.read()

setup(
    name='drf-extra-utils',
    version='0.0.5',
    license='MIT License',
    author='Gabriel Lustosa',
    long_description=README,
    long_description_content_type="text/markdown",
    packages=['drf_extra_utils', 'drf_extra_utils.annotations', 'drf_extra_utils.related_object'],
    author_email='lustosaki2@gmail.com',
    description='Utils for django rest',
    python_requires=">=3.8",
)
