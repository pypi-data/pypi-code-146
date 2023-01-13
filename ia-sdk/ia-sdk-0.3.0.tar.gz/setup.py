import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ia-sdk",
    version="0.3.0",
    author="Intelligent Artifacts",
    author_email="support@intelligent-artifacts.com",
    description="SDK for Intelligent Artifact's GAIuS agents.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://intelligent-artifacts.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'requests',
          'pymongo',
	      'plotly'
      ],
)
