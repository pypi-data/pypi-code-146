import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mmpxrt",
    version="1.13",
    author="Michal Smid",
    author_email="m.smid@hzdr.de",
    description="Raytracing code for x-ray (mosaic) spectrometers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.hzdr.de/smid55/mmpxrt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
