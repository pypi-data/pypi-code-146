import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyailab",
    version="0.0.3",
    description='artificial intelligence',
    license='MIT',
    author="aiml department",
    author_email="aiml5thsem@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['artificial intelligence lab', 'ailab'],
    python_requires='>=3.7',
    py_modules=['pyailab'],
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = []
)