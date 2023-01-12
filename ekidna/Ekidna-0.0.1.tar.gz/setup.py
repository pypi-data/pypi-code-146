from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Science/Research',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Ekidna',
    version='0.0.1',
    description='Electrochemistry data analysis tools',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='OzymandiasTheDead',
    author_email='jacob@ekidnasensing.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Ekidna',
    packages=find_packages(),
    install_requires=['']
)
