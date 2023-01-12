import setuptools
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), "r", encoding="utf-8") as fp:
    long_description = fp.read()

setuptools.setup(
    name="aclient",
    version="1.0.7",
    url="https://github.com/PengKe-x/AsyncHttpClient",
    author="PengKe",
    author_email="925330867@qq.com",
    description="发送大量异步请求",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["aiohttp", "yarl"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
