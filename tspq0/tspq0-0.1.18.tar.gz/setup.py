

from setuptools import setup, find_packages

with open('requirements.txt') as file:
    INSTALL_REQUIERES = file.read().splitlines()

setup(
	author="Mars Mel",
	description="Travelling salesman problem by qiskit",
	name="tspq0",
	version="0.1.18",
	py_modules=["tspq0"],
	packages=find_packages(include=['tspq0']),
	install_requires= INSTALL_REQUIERES
	
	)





						
