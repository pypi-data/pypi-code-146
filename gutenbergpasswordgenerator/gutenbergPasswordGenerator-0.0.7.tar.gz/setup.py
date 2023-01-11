import setuptools
import versioneer

with open("README.rst", "r") as f:
    long_description = f.read()
with open("requirements.txt", "r") as f:
    requirements = [line.strip() for line in f]

setuptools.setup(
    name="gutenbergPasswordGenerator",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Matthew Ivancic",
    author_email="matthew.ivancic91@gmail.com",
    description= "Python library to generate passwords using the text of classic novels",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
)
