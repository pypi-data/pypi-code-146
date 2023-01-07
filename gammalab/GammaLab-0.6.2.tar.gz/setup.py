from setuptools import setup, find_packages

setup(
    name='GammaLab',
    version='0.6.2',
    description='Toolkit for soundcard gamma ray spectroscopy',
    author='F.I. Pelupessy',
    url='https://github.com/ipelupessy/gammalab',
    license='GPLv3',
    packages=find_packages('src'),
    package_data={},
    package_dir={'' : 'src'},
    install_requires=['wheel', 'numpy', 'SoundCard', 'matplotlib'],
    python_requires='>=3.6',
    scripts=['bin/gammalab-histogram.py', 'bin/gammalab-monitor.py','bin/gammalab-calibration-calc.py'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3) ',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    long_description=open('README.rst').read(),
)
