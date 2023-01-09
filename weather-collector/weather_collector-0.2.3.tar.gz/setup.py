from setuptools import setup, find_packages

with open("README.md", "r") as fh:

    long_description = fh.read()


setup(
    name="weather_collector",
    version="0.2.3",
    packages=find_packages(include=["weather_collector*"]),
    include_package_data=True,
    install_requires=["Click", "bulkhead", "amarium"],
    entry_points={
        "console_scripts": [
            "weather-collector = weather_collector.sampler:sample",
        ],
    },
    author="Julian M. Kleber",
    author_email="julian.kleber@sail.black",
    description="CLI for collecting weather data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codeberg.org/cap_jmk/weather-collector",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
