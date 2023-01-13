import codefast as cf
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = setuptools.find_packages()
print(packages)
data = [f.lstrip('fastnsq/') for f in cf.io.walk('fastnsq/bins/')]

setuptools.setup(
    name="fastnsq",
    version="0.0.5",
    author="slipper",
    author_email="r2fscg@gmail.com",
    description="NULL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/private_repo/uuidentifier",
    packages=setuptools.find_packages(),
    package_data={'fastnsq': data},
    install_requires=['codefast', 'fire', 'simauth', 'asyncio'],
    entry_points={'console_scripts': [
        'fastnsq=fastnsq.app:main',
    ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
