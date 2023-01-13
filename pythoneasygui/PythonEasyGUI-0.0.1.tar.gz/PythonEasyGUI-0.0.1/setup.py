from setuptools import setup

with open("gui/README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='PythonEasyGUI',
    version='0.0.1',
    packages=['gui'],
    url='https://github.com',
    license="MIT",
    author='Yvan',
    author_email='yvan_chen2022@163.com',
    description='This is a easy gui',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.8',
)
