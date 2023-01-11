import setuptools
import os

with open('README.md') as readme_f:
  long_description = readme_f.read()

packages = setuptools.find_packages()
for root, _, files in os.walk("tecton_proto"):
  if any([f.endswith("_pb2.py") for f in files]):
    packages.append(root.replace("/", "."))
for root, _, files in os.walk("protoc_gen_swagger"):
  if any([f.endswith("_pb2.py") for f in files]):
    packages.append(root.replace("/", "."))

setuptools.setup(
    classifiers=['Programming Language :: Python :: 3', 'Operating System :: OS Independent', 'License :: Other/Proprietary License'],
    python_requires='>=3.7.*',
    author='Tecton, Inc.',
    author_email='support@tecton.ai',
    url='https://tecton.ai',
    license='Tecton Proprietary',
    include_package_data=True,
    description='Tecton Python SDK',
    entry_points={'console_scripts': ['tecton=tecton.cli.cli:main'], 'pytest11': ['pytest_tecton=tecton.pytest_tecton']},
    name='tecton',
    version='0.6.0b40',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['attrs>=21.3.0', 'boto3', 'googleapis-common-protos~=1.52', 'jinja2~=3.0.3', 'numpy~=1.16', 'pathspec', 'pendulum~=2.1', 'protobuf~=3.20.1', 'pyarrow~=8.0.0', 'pypika~=0.48.9', 'pytimeparse', 'pandas~=1.0', 'texttable', 'requests', 'colorama~=0.4', 'tqdm~=4.41', 'yaspin~=0.16', 'typing-extensions~=4.1', 'pygments>=2.7.4', 'pytest', 'click~=8.0', 'typeguard', 'sqlparse', 'semantic_version'],
    extras_require={'databricks-connect': ['databricks-connect~=9.1.23'], 'databricks-connect9': ['databricks-connect~=9.1.23'], 'databricks-connect10': ['databricks-connect~=10.4.12'], 'pyspark': ['pyspark~=3.1.2'], 'pyspark3': ['pyspark~=3.1.2'], 'pyspark3.1': ['pyspark~=3.1.2'], 'pyspark3.2': ['pyspark~=3.2.1'], 'snowflake': ['snowflake-connector-python~=2.8'], 'snowpark': ['snowflake-snowpark-python~=1.0.0'], 'athena': ['awswrangler~=2.15']},
    packages=packages,
)
