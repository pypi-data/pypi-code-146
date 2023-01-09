import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gTixi",
    version="0.1.0",
    author="Spectre Lee",
    author_email="lxwk1spectre@foxmail.com",
    description="高效碳基演示体系",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/lxwk1spectre/walartminstar",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)