from setuptools import find_packages, setup

requirements = []
with open("requirements.txt", encoding="UTF-8") as f:
    requirements = f.read().splitlines()

readme = ""
with open(f"README.md", encoding="UTF-8") as f:
    readme = f.read()

setup(
    name="twitch-thumbnail",
    version="1.1.0",
    description="Download Twitch channel thumbnail",
    author="Minibox",
    author_email="minibox724@gmail.com",
    url="https://github.com/minibox24/twitch-thumbnail",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    packages=find_packages(),
    python_requires=">=3.9",
)
