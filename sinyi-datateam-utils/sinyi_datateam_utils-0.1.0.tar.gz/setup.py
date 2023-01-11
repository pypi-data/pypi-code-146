
import setuptools
  
with open("README.md", "r") as fh:
    description = fh.read()
  
setuptools.setup(
    name="sinyi_datateam_utils",
    version="0.1.0",
    author="sinyidatateam",
    author_email="me30@sinyi.com.tw",
    packages=["sinyi_utils"],
    description="Utilities for data analysis",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://SinyiDataTeam@dev.azure.com/SinyiDataTeam/Label360/_git/sinyi_utils",
    license='MIT',
    python_requires='>=3.8',
    install_requires=["pycryptodome", "pandas-gbq","google-cloud-storage","azure-identity",
    "azure-keyvault-secrets"]
)