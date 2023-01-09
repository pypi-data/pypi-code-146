from setuptools import setup

setup(
    name='keap_flask',
    version='0.4.0',
    description='A Rest Client For Flask applications',
    author='will sexton',
    author_email='will@theapiguys.com',
    url='https://github.com/codinlikewilly/keap_flask',
    readme = "README.md",
    license='BSD 2-clause',
    packages=['keap_flask'],
    install_requires=['Flask',
                      'AuthLib',
                      'python-dateutil',
                      'requests'
                      ],

    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
)
