import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ffAlive",
    version="1.0.4",
    author="Tim Green",
    author_email="the.green.timtam@gmail.com",
    description="FFMPEG with Progress Bars",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/packagename",
    packages=[ 'ffAlive' ],
    install_requires  = ['alive_progress', 'ffmpeg_progress_yield'],
    license = 'MIT'
)
