from setuptools import find_packages, setup
setup(
    name='example777',
    packages=find_packages(include=['example777']),
    version='0.1.0',
    description='Test package to demonstrate how to build packages',
    author='M.O.',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.1.2'],
    test_suite='tests'
)