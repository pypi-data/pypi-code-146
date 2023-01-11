from setuptools import find_packages, setup
import os


def _instantiate_sca3s_config():
    """
    Instantiates the SCA3S config system.
    """
    home = os.path.expanduser('~')
    try:
        os.mkdir(home + '/.sca3s')
    except:
        pass
    try:
        with open(home + '/.sca3s/config', 'x') as _:
            pass
    except:
        pass

with open('README.md') as fd:
    readme = fd.read()

setup(
    name='sca3s_cli',
    version='1.0.6',
    author='James Webb',
    author_email='james.webb@bristol.ac.uk',
    license='Apache2',
    url='https://github.com/jwsi/sca3s-cli',
    description="Toolkit to enable job submission to SCA3S from the command line",
    packages=find_packages(),
    keywords="sca3s sca3s_cli",
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',

        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',

        'Programming Language :: Python :: 3',

        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries',
    ],
    zip_safe=True,

    # Require requests library
    install_requires=["requests>=2.27", "rich>=12.5.1"],

    entry_points = """
        [console_scripts]
        sca3s-cli=sca3s_cli.cli:main
    """
)

_instantiate_sca3s_config()
