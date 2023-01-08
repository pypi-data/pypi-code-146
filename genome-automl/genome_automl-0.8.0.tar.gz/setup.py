import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="genome_automl", # Replace with your own username
    version="0.8.0",
    license='MIT',
    author="Endri Del",
    author_email="endrideliu@gmail.com",
    description="library for highly scalable AutoML pipelines, apps and evaluations, deploy ML platform on AWS, Google Cloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edeliu2000/genome",
    package_dir={"": "."},
    packages=setuptools.find_packages(exclude=["test.*", "test"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
