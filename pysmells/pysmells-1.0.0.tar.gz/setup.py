from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='pysmells',
    version='1.0.0',
    license='MIT License',
    author='Marco Aurélio Proença Neto, Marcos Paulo Alves de Sousa',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='desousa.mpa@gmail.com',
    keywords='pysmells',
    description=u'Pysmells é um pacote Python que identifica e gera relatórios de erros no seu código Python',
    packages=['pysmells'],
    install_requires=['autopep8', 'pylint', 'mypy', 'pandas'],
    url='https://github.com/pysmells/pysmells'
    )
