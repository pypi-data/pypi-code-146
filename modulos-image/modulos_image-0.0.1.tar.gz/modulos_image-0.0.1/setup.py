from setuptools import setup, find_packages
import request

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="modulos_image",
    version="0.0.1",
    author="MARCIOXANDIR",
    author_email="marcioalexdias@gmail.com",
    description="My short description",
    long_description=page_description,
    long_description_content_type="text/markdown",
    packages=['image_package'], # aqui a lista dos metodos
    install_requires=requirements, # variavel com texto de descrição
    python_requires='>=3.8',
)