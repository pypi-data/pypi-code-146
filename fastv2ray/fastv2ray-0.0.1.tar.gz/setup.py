import codefast as cf
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = setuptools.find_packages()
data = [f.lstrip('fastv2ray/') for f in cf.io.walk('fastv2ray/bins/')]
data.extend([f.lstrip('fastv2ray/') for f in cf.io.walk('fastv2ray/configs/')])

setuptools.setup(
    name="fastv2ray",
    version="0.0.1",
    author="slipper",
    author_email="r2fscg@gmail.com",
    description="NULL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://google.com",
    packages=setuptools.find_packages(),
    package_data={'fastv2ray': data},
    install_requires=['codefast', 'fire', 'simauth', 'asyncio'],
    entry_points={'console_scripts': [
        'fastv2ray=fastv2ray.app:main',
    ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
