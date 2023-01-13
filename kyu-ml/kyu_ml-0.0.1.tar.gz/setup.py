import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kyu_ml",
    version="0.0.1",
    author="kyunam",
    author_email="rbska56455@gmail.com",
    description="personal library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kyu90/kyu_personal",
    project_urls={
        "Bug Tracker": "https://github.com/kyu90/kyu_personal/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)