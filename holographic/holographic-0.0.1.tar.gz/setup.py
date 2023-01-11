import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="holographic",
    version="0.0.1",
    author="Max Taggart",
    author_email="max.taggart@healthcatalyst.com",
    description="This is ground control to Major Tom...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "click~=8.1.3",
        "cryptography~=39.0.0",
        "Flask~=2.2.2",
        "gunicorn~=20.1.0",
        "pydantic~=1.10.2",
        "requests~=2.28.1",
        "rich~=13.0.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
