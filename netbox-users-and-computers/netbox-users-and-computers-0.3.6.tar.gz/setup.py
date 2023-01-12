from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='netbox-users-and-computers',
    version='0.3.6',
    description='Netbox plugin. Manage AD Users and Workstations',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    download_url='https://pypi.org/project/netbox-users-and-computers/',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords=['netbox', 'netbox-plugin'],
    author='Artur Shamsiev',
    author_email='me@z-lab.me',
    maintainer='Artur Shamsiev',
    maintainer_email='me@z-lab.me',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
