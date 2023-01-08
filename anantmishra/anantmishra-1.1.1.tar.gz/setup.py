from setuptools import setup
setup(
    name='anantmishra',
    version='1.1.1',
    py_modules=['anant'],
    install_requires=[],
    author='Anant Mishra',
    author_email='gioneemaxuser@gmail.com',
    description='A simple package for doing calculations \n commands list: \n calculate(x, y, operation) \n about() \n operations: "add" "subtract" "divide"  "exponentiate" "modulo" "square root"  ',
    url='https://github.com/Slowloris01',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    long_description=open('README.md').read(),
)
