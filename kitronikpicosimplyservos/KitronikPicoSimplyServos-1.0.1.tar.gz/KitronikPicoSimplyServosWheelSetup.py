from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = "KitronikPicoSimplyServos",
    version = "1.0.1",
    description = "Kitronik Simply Servo board for Raspberry Pi Pico allows for up to 8 servos to be controlled simultaneously",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    py_modules = ["SimplyServos"],
)