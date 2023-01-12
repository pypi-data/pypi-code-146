from setuptools import setup


setup(
    name='spider-core-sdk',
    version='1.4.8',
    author='wog',
    description='',
    packages=['spider_core'],
    include_package_data=True,
    python_requires='>=3.7',
    entry_points="""
    [console_scripts]
    cjzt=spider_core.main:main
    """,
    install_requires=['likeshell>=1.1.5', 'jinja2', 'requests', 'termcolor'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
)
