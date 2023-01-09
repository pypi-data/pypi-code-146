import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tempailab",
    version="0.0.7",
    description='artificial intelligence and DBMS lab programs definitions',
    license='MIT',
    author="aiml department",
    author_email="aiml5thsem@gmail.com",
    url = 'https://github.com/aiml5thsem/tempailab',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['artificial intelligence lab', 'DBMS lab', 'aimllab module'],
    python_requires='>=3.7',
    py_modules=['tempailab'],
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'numpy'
    ]
)