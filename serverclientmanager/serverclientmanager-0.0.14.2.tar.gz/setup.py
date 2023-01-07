from setuptools import setup, find_packages

VERSION = "0.0.14.2"
DESCRIPTION = "authenticate and send files to a server and back"

# Setting up
setup(
    name="serverclientmanager",
    version=VERSION,
    author="Theo Tappe",
    author_email="<tappetheo@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["werkzeug"],
    keywords=["python", "sockets"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
