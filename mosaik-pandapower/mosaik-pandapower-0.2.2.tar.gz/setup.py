from setuptools import setup, find_packages

setup(
    name='mosaik-pandapower',
    version='0.2.2',
    author='Rami Elshinawy',
    author_email='mosaik@offis.de',
    description='An adapter to use pandapower with mosaik.',
    long_description=(open('README.rst', encoding='utf-8').read() + '\n\n' + 
                      open('CHANGES.txt', encoding='utf-8').read() + '\n\n' + 
                      open('AUTHORS.txt', encoding='utf-8').read()),
    long_description_content_type='text/x-rst',
    url='https://gitlab.com/mosaik/components/energy/mosaik-pandapower',
    install_requires=[
        'arrow>=1.0',
        'mosaik-api>=2.0',
        'pandapower',
        'matplotlib',
        'numba',
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mosaik-pandapower = mosaik_pandapower.simulator:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
    ],
)
