import setuptools

import rpu

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.read().splitlines()

setuptools.setup(
    name="rpu",
    author="cibere",
    author_email="cibere.dev@gmail.com",
    url="https://github.com/cibere/rpu",
    project_urls={
        "Code": "https://github.com/cibere/rpu",
        "Issue tracker": "https://github.com/cibere/rpu/issues",
        "Discord/Support Server": "https://discord.gg/2MRrJvP42N",
    },
    version=rpu.__version__,
    python_requires=">=3.9",
    install_requires=REQUIREMENTS,
    packages=["rpu", "rpu.librarys"],
    description=rpu.__description__,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
)
