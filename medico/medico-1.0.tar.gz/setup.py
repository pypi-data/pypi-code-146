from setuptools import setup

setup(name="medico",
version="1.0",
description="Extract vital medical information from text.",
long_description="This package extracts vital health information from string such as medicine names, dosage, treatment names, diagnostic data, etc.",
author="Mr. Medico",
packages=["medico"],
install_requires=['boto3', 'time', 'spacy', 'nltk'])