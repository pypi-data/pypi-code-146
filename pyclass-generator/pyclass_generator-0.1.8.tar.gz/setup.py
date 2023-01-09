from setuptools import setup

setup(
    name='pyclass_generator',
    version='0.1.8',
    description='This is a package to generate python class from a nested dictionary',
    url='https://github.com/Venus713/pyclass-generator',
    author='Venus713',
    author_email='userstar713@gmail.com',
    license='MIT',
    packages=[
        'pyclass_generator'
    ],
    install_requires=["libcst", "gitpython", "datamodel-code-generator"],
    zip_safe=False
)
