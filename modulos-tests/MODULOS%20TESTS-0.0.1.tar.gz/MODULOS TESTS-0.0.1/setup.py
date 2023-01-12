from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="MODULOS TESTS",
    version="0.0.1",
    author="MARCIO DIAS",
    author_email="marcioalexdias@gmail.com",
    description="My short description",
    long_description=page_description,
    long_description_content_type="text/markdown",
    # url="my_github_repository_project_link",
    packages=['CALCULADORAMINHA'], # aqui a lista dos metodos
    install_requires=requirements, # variavel com texto de descrição
    python_requires='>=3.8',
)