from setuptools import setup

long_desciption: str = """
This Package can be used from Debugging purposes.
When you are working in long project, you often use print statement for debugging purposes.
Sometime, you use to many print statement and after completing debugging you spent sometime to find and remove all those previous print statement

What does this package do?
When you print something for debugging purposes using this package, it will print out in following pattern

[TYPE_OF_WARNING] -> TextType (INFO, WARNING, etc)
[From] -> Which method is calling this packages' method
[Line] -> On which line is it calling
[Statement(s)] -> Print all the messages you have writen

You can even pass multiple texts as parameters just like in print statement

Example
from package_logger import LoggerClass, TextType

logger = LoggerClass()
logger.print("Hello", "World", type_ = TextType.INFO)

You can use colorPrint method instead of print method to print with color for different messages type
Example
from package_logger import ColorType
logger.colorPrint("Hello", "World", type_ = TextType.INFO, color = ColorType.COLOR_INFO)
"""

setup(
    name='package_logger',
    version='1.0.0',
    description='Logger for Python',
    long_description=long_desciption,
    long_description_content_type='text/markdown',
    keywords='python3-logger logger debugging print',
    author='Sachin Acharya',
    author_email='acharyaraj71+logger@gmail.com',
    packages=['package_logger'],
    install_requires = ['colorama'], # pathlib2
    url='https://github.com/sachin-acharya-projects/package_logger',
    package_data={
        '': ['package_logger.py']
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)

# python .\setup.py sdist bdist_wheel