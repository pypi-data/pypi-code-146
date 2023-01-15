from setuptools import find_packages, setup

__VERSION__ = "1.0.1.37"

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()
with open("LICENSE.txt", "r", encoding="utf-8") as f:
    lcs = f.read()

setup(
    name="otsutil",
    version=__VERSION__,
    url="https://github.com/Otsuhachi/Otsutil",
    description="個人的によく使う関数、クラス、型ヒントを纏めたライブラリです。",
    long_description_content_type="text/markdown",
    long_description=readme,
    author="Otsuhachi",
    author_email="agequodagis.tufuiegoeris@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    license=lcs,
    python_requires=">=3.7",
)
