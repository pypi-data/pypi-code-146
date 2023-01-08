import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="autom8it",
    version="1.2.2",
    author="Eldad Bishari",
    author_email="eldad@1221tlv.org",
    description="Automate IT operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eldad1221/autom8it",
    packages=setuptools.find_packages(),
    install_requires=[
        'PyYAML==6.0',
        'pytz==2021.3',
        'cerberus==1.3.4',
        'boto3==1.26.3',
        'requests==2.28.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
