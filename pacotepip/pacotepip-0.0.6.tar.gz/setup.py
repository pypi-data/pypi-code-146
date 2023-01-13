from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='pacotepip',
    version='0.0.6',
    url='https://github.com/diogjunior100/pacotepip.git',
    license='MIT License',
    author='Diogenes e Igor',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='diogjunior10071@gmail.com',
    keywords='Pacote',
    description=u'Exemplo de pacote PyPI',
    packages=['pacotepip'],
    install_requires=[''],)
