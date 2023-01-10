import setuptools

with open("README.rst", "r") as file:
    long_description=file.read()

setuptools.setup(
    name="full-watch-avatar-2-the-way-of-water-2022-online-on-123movies",
    version="1.2",
    author="Vikram Shinde",
    author_email="sinden@gmail.com",
    description="Python project for testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://toptoday.live",
    packages=setuptools.find_packages(exclude=['tests*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=2.7',
    include_package_data=True,
    install_requires=[]
)