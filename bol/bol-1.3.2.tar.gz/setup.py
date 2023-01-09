import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bol",
    version="1.3.2",
    author="Stein van Broekhoven",
    author_email="stein@aapjeisbaas.nl",
    description="A bol.com api connector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/aapjeisbaas/bol",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests'
    ]
)