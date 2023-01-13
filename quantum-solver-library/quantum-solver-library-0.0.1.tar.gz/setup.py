from setuptools import setup
 
setup(
    name='quantum-solver-library',
    packages=[''], # Mismo nombre que en la estructura de carpetas de arriba
    version='0.0.1',
    license='MIT License', # La licencia que tenga tu paquete
    long_description='A little quantum toolset developed using Qiskit',
    description='A little quantum toolset developed using Qiskit',
    author='Andrea Hernández',
    author_email='alu0101119137@ull.edu.es',
    url='https://github.com/alu0101119137/quantum-solver.git', # Usa la URL del repositorio de GitHub
    download_url='https://github.com/alu0101119137/quantum-solver/archive/v0.1.tar.gz', # Te lo explico a continuación
    keywords='quantum solver using Qiskit', # Palabras que definan tu paquete
    classifiers=['Programming Language :: Python',  # Clasificadores de compatibilidad con versiones de Python para tu paquete
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7'],
)