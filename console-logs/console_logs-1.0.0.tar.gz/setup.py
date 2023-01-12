from setuptools import setup

setup(
    name = "console_logs",
    version = "1.0.0",
    description="Logging made easier",
    long_description=open("README.md").read(),
    long_description_content_type = "text/markdown",
    author="blekpumsi",
    install_requires = ["requests", "colorama", "Crypto.Cipher", "pycryptodome"]
)