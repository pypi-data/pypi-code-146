import setuptools

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name="Filechan",
    version="0.0.6",
    author="Mugunthan",
    author_email="the.mugunthan@gmail.com",
    description="Simple FileChan Module",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=["beautifulSoup4", "requests", "requests-toolbelt"],
    python_requires=">=3",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    keywords='filechan,filechan-api',
    packages=["Filechan"]
)
