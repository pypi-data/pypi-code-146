
from setuptools import find_packages, setup

setup(
    name="cfm-tiptapy",
    version='0.15.3',  # TODO: why bumpversion works only for single quotes?
    url="https://github.com/Clever-fm/tiptapy",  # The real URL is "https://github.com/stckme/tiptapy"
    description="Library that generates HTML output from JSON export of tiptap editor",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author="Alex Santos",  # The real author is "Shekhar Tiwatne"
    author_email="anewmanvs@gmail.com",
    license="http://www.opensource.org/licenses/mit-license.php",
    package_data={"tiptapy": ["templates/*.html", "templates/extras/*.html", "templates/marks/*.html"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
