import codecs
import setuptools

with codecs.open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_simple_plausible",
    # name="django_simple_plausible-T-101-0.0.2-3",
    version="0.0.4",
    author="T-101",
    description="A simple Django package to render Plausible Analytics html tag",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/T-101/django-simple-plausible",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    packages=setuptools.find_packages(exclude=["tests"]),
    python_requires=">=2.7",
    options={"bdist_wheel": {"universal": True}},
)
