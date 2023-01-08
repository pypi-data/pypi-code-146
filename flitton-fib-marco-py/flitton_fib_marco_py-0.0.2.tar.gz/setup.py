from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="flitton_fib_marco_py",
    version="0.0.2",
    author="Marco Paspuel",
    author_email="marco.paspuel@outlook.com",
    description="Calculates a Fibonacci number",
    long_description=long_description,
    long_description_context_type="text/markdown",
    url="https://github.com/marcopaspuel/flitton-fib-py",
    install_requires=[
        "PyYAML>=4.1.2",
        "drill>=0.2.8",
    ],
    packages=find_packages(exclude="tests,"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    test_require=['pytest'],
    extras_require={
        'server': ["Flask>=1.0.0"]
    },
    entry_points={
        'console_scripts': ['fib-number = flitton_fib_py.cmd.fib_numb: fib_numb', ],
    },
)
