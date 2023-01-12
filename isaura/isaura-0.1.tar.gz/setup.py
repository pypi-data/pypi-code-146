import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = [
    "h5py==3.7.0",
    "loguru==0.6.0"
]

setuptools.setup(
    name="isaura",
    version="0.1",
    author="Ersilia Open Source Initiative",
    author_email="hello@ersilia.io",
    description="Isaura data lake for pre-computed Ersilia properties",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ersilia-os/isaura",
    project_urls={"GitBook": "https://ersilia.gitbook.io/ersilia/",},
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=["utilities"]),
    python_requires=">=3.7",
)
