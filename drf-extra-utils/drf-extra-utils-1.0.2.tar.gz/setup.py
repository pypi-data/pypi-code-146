from setuptools import setup

with open('README.md') as readme:
    README = readme.read()

setup(
    name='drf-extra-utils',
    version='1.0.2',
    license='MIT License',
    author='Gabriel Lustosa',
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=['Django==4.1.5', 'djangorestframework==3.14.0'],
    packages=['drf_extra_utils', 'drf_extra_utils.annotations', 'drf_extra_utils.related_object'],
    author_email='lustosaki2@gmail.com',
    description='Utils for django rest',
    python_requires=">=3.8",
)
