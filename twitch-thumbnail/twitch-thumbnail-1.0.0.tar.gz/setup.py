from setuptools import find_packages, setup

requirements = []
with open("requirements.txt", encoding="UTF-8") as f:
    requirements = f.read().splitlines()

setup(
    name="twitch-thumbnail",
    version="1.0.0",
    description="Download Twitch channel thumbnail",
    author="Minibox",
    author_email="minibox724@gmail.com",
    url="https://github.com/minibox24/twitch-thumbnail",
    install_requires=requirements,
    packages=find_packages(),
    python_requires=">=3.9",
)
