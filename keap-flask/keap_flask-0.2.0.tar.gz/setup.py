from setuptools import setup

setup(
    name='keap_flask',
    version='0.2.0',
    description='A Rest Client For Flask applications',
    author='will sexton',
    author_email='will@theapiguys.com',
    url='https://github.com/codinlikewilly/keap_flask',
    license='BSD 2-clause',
    packages=['keap_flask'],
    install_requires=['Flask',
                      'AuthLib',
                      'python-dateutil'
                      ],

    classifiers=[
        'License :: OSI Approved :: BSD License'
    ],
)
