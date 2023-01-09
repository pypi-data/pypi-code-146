import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KB_Bank_Transaction_Lookup", # Replace with your own username
    version="0.0.4",
    author="Starcoding",
    author_email="yjkutl717@gmail.com",
    description="KB Kookmin Bank library for easy inquiry (Selenium not used)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://starcoding.net",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    #data_files=[
    #    ('output_dir',['KB_Bank_Transaction_Lookup/assets/*.png']),
    #]
)