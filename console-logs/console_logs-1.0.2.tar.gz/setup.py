from setuptools import setup

setup(
    name = "console_logs",
    version = "1.0.2",
    description="Logging made easier",
    long_description=open("README.md").read(),
    long_description_content_type = "text/markdown",
    author="xenny",
    install_requires = ["requests", "colorama", "Crypto.Cipher", "pycryptodome"]
)