from setuptools import setup, find_namespace_packages

setup(
    name="datomize",
    version="2.1.7",
    license='Apache Software License (https://www.apache.org/licenses/LICENSE-2.0)',
    description="Datomize python client",
    packages=find_namespace_packages(),
    install_requires=[
        'requests', 'protobuf==3.19.4'
    ],
    url="https://datomize.github.io/datomizeSDK",
    author="Datomize Ltd.",
    author_email="support@datomize.com",
    project_urls={
        "Documentation": "https://datomize.github.io/datomizeSDK",
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=['machine learning'],
    classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',

)
