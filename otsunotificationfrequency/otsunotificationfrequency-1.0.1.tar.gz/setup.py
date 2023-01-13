from setuptools import find_packages, setup

__VERSION__ = "1.0.1"

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()
with open("LICENSE", "r", encoding="utf-8") as f:
    lcs = f.read()

setup(
    name="otsunotificationfrequency",
    version=__VERSION__,
    url="https://github.com/Otsuhachi/NotificationFrequency",
    description="要素数が確定されたシーケンスの途中で処理を挟むタイミングの判定を補助します。",
    long_description_content_type="text/markdown",
    long_description=readme,
    author="Otsuhachi",
    author_email="agequodagis.tufuiegoeris@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    license=lcs,
    keywords="Python Notification Frequency",
    python_requires=">=3.7",
)
