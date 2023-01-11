import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt','r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
    # pip3 Fxlifestyle Course Free Download
    name="Fxlifestyle Course Free Download", 
    version="1",
    author="Fxlifestyle Course Free Download",
    author_email="FreeDownloadFxlifestyle@Fxlifestyle.com",
    description="Fxlifestyle Course Free Download",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://cab2cbhjtozy8x12adw8nk0z6d.hop.clickbank.net/?tid=py",
    project_urls={
        "Bug Tracker": "https://github.com/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=requires,
)
