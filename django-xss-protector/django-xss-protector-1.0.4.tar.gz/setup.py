import setuptools

setuptools.setup(
    name="django-xss-protector",  # should be unique in pypi packages
    version="1.0.4",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    # these packages will be excluded
    packages=setuptools.find_packages(exclude=["tests", "data", "test"])
)
