from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='easy-pyinstaller',
    version='0.0.21',
    license='MIT License',
    author='Igor Polegato',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='',
    keywords='ip-pyinstaller',
    description=readme,
    packages=['easy_pyinstaller'],
    install_requires=['pyinstaller'],)
