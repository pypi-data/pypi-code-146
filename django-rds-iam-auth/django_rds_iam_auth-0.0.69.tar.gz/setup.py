import re

from setuptools import find_packages, setup

version = '0.0.69'

docs_require = []

tests_require = [
    "coverage",
    "pretend",
    "pytest",
    "pytest-cov",
    "pytest-mock",
    "pytest-django",
]


with open("README.md") as fh:
    long_description = re.sub(
        "<!-- start-no-pypi -->.*<!-- end-no-pypi -->\n",
        "",
        fh.read(),
        flags=re.M | re.S,
    )

setup(
    name="django_rds_iam_auth",
    version=version,
    description="Django database backends to use AWS Database IAM Authentication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LabD/django-iam-dbauth",
    author="Lab Digital",
    author_email="admin@ibrag.me",
    install_requires=["Django>=1.11", "boto3", "dnspython"],
    tests_require=tests_require,
    extras_require={"docs": docs_require, "test": tests_require},
    entry_points={},
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False,
)
