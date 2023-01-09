from copy import deepcopy
from typing import Dict, List

import setuptools

__base_version__ ="0.15.21"
__version__ ="0.15.21-rc.0"

requirements = [
    "gorilla==0.4.0",
]

airflow_packages = ["openlineage-airflow==0.6.1"]

dbt_packages = [
    "dbt-core>=1.0.0",
    "dbt-bigquery>=1.0.0",
]

# For local development:
# pip install .
# poetry install --extras "airflow"
# Published packages:
# - pip install "alvin-integration[dbt]"
# - pip install "alvin-integration[airflow]"
INTEGRATION_EXTRAS_DEPENDENCIES: Dict[str, List[str]] = {
    "dbt": dbt_packages,
    "airflow": airflow_packages,
}

EXTRAS_DEPENDENCIES: Dict[str, List[str]] = deepcopy(INTEGRATION_EXTRAS_DEPENDENCIES)


setuptools.setup(
    name="alvin_integration",
    version=__version__,
    author="Alvin",
    author_email="tech@alvin.ai",
    description="Alvin lineage python library for integrations",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    extras_require=EXTRAS_DEPENDENCIES,
    python_requires=">=3.7",
)
