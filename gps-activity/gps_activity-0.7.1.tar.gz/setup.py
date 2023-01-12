# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gps_activity',
 'gps_activity.extraction',
 'gps_activity.extraction.factory',
 'gps_activity.extraction.factory.classifiers',
 'gps_activity.extraction.factory.clustering',
 'gps_activity.extraction.factory.fragmentation',
 'gps_activity.extraction.nodes',
 'gps_activity.linker',
 'gps_activity.linker.factory',
 'gps_activity.linker.nodes',
 'gps_activity.metrics',
 'gps_activity.metrics.nodes',
 'gps_activity.nodes']

package_data = \
{'': ['*']}

install_requires = \
['Rtree>=1.0.0,<2.0.0',
 'geopandas>=0.11.1,<0.12.0',
 'numpy>=1.23.1,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pandera>=0.11.0,<0.12.0',
 'pygeos>=0.12.0,<0.13.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'scipy>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'gps-activity',
    'version': '0.7.1',
    'description': 'A light-weight mobile module for analysis of GPS activity',
    'long_description': '# **GPS activity** 🚛\n\n![Python versions](https://img.shields.io/pypi/pyversions/gps_activity)\n![Latest release](https://img.shields.io/github/v/release/WasteLabs/gps_activity)\n![Latest release date](https://img.shields.io/github/release-date/WasteLabs/gps_activity)\n![License](https://img.shields.io/github/license/WasteLabs/gps_activity)\n[![CI test](https://github.com/WasteLabs/gps_activity/actions/workflows/ci-tests.yaml/badge.svg)](https://github.com/WasteLabs/gps_activity/actions/workflows/ci-tests.yaml)\n[![codecov](https://codecov.io/gh/WasteLabs/gps_activity/branch/main/graph/badge.svg?token=58AY7B1YBB)](https://codecov.io/gh/WasteLabs/gps_activity)\n\nA light-weight module for analysis of GPS activity. Package is designed to be trade-off solution for both researchers and developers in Waste Labs. Using `gps_activity` you can:\n\n1. Cluster your time-series gps records to extract activity points\n2. Join activity points with original plan or operation report\n3. Estimate clustering performance\n\n## Installation ☁️ -> 🖥️\n\nUsing pip:\n\n```bash\npip3 install gps_activity\n```\n\n## **Python package modules** 📦\n\n---\n\n- **extraction**: clusters GPS records and extracts cluster activities ([checkout module structure]((https://github.com/WasteLabs/gps_activity/tree/main/docs/extraction/README.md)))\n- **linker**: joins route plan and clustered gps records\n- **metrics**: estimates clustering performance based on:\n    1. internal source: ones that based on inter & intra cluster distances\n    2. external source: joined route plan and clustered gps records (output of **linker** module)\n\n![components](docs/diagrams/gps_activity_components.png)\n\n## **Extraction modules** 🔵 🟣 ⚫️\n\n---\n\nOrganized by preprocessing, fragmentation & clustering steps that ultimately are packed into `ActivityExtractionSession` object and orchestrated.\n\n### ⚠️ `ActivityExtractionSession` assumptions and constrains\n\n1. 1 vehicle = 1 session run: to avoid clusters overlap\n1. No duplicated gps records over vehicle-timstamp: avoids division by zero during computing `velocity`\n\n### 🚀 **VHFDBSCAN**: Velocity hardlimit fragmentation Density-based spatial clustering of applications with noise\n\n- Fragmentation is performing by applying hardlimiting on velocity computed from `lat`, `lon` and `datetime` columns\n- Clustering is performed by classical DBSCAN that considers non-cluster candidates as noise\n\n```python\nfrom gps_activity import ActivityExtractionSession\nfrom gps_activity.extraction.factory.preprocessing import PreprocessingFactory\nfrom gps_activity.extraction.factory.fragmentation import VelocityFragmentationFactory\nfrom gps_activity.extraction.factory.clustering import FDBSCANFactory\n\n\npreprocessing = PreprocessingFactory.factory_pipeline(\n    source_lat_column="lat",\n    source_lon_column="lon",\n    source_datetime="datetime",\n    source_vehicle_id="plate_no",\n    source_crs="EPSG:4326",\n    target_crs="EPSG:2326",\n)\n\nfragmentation = VelocityFragmentationFactory.factory_pipeline(max_velocity_hard_limit=4)\nclustering = FDBSCANFactory.factory_pipeline(eps=30, min_samples=3)\n\nactivity_extraction = ActivityExtractionSession(\n    preprocessing=preprocessing,\n    fragmentation=fragmentation,\n    clustering=clustering,\n)\n\nactivity_extraction.predict(gps)\n```\n\n### 🚀 **VHFSTCM**: Velocity hardlimit fragmentation spatio-temporal clustering model\n\n- Fragmentation is performing by applying hardlimiting on velocity computed from `lat`, `lon` and `datetime` columns\n- Clustering is performed according steps:\n    1. Generated adjacent proximity mask (if cluster pair distance <= `eps`)\n    2. Clusters ID are generated according: proximity mask and fragmentation flag\n    3. GPS records grouped by `cluster_id` and aggregated cluster time span\n    4. Cluster is validated if time span >= `min_duration_sec`\n    5. Validated cluster ids are set to original GPS records\n\n```python\nfrom gps_activity import ActivityExtractionSession\nfrom gps_activity.extraction.factory.preprocessing import PreprocessingFactory\nfrom gps_activity.extraction.factory.fragmentation import VelocityFragmentationFactory\nfrom gps_activity.extraction.factory.clustering import STCMFactory\n\n\npreprocessing = PreprocessingFactory.factory_pipeline(\n    source_lat_column="lat",\n    source_lon_column="lon",\n    source_datetime="datetime",\n    source_vehicle_id="plate_no",\n    source_crs="EPSG:4326",\n    target_crs="EPSG:2326",\n)\n\nfragmentation = VelocityFragmentationFactory.factory_pipeline(max_velocity_hard_limit=4)\nclustering = STCMFactory.factory_pipeline(\n    source_vehicle_id_column="plate_no",\n    eps=30,\n    min_duration_sec=60\n)\n\nstcm = ActivityExtractionSession(\n    preprocessing=preprocessing,\n    fragmentation=fragmentation,\n    clustering=clustering,\n)\n```\n\n## Linker module implementation 🔵 🟣 ⚫️\n\n**[Overview linker module components](https://github.com/WasteLabs/gps_activity/tree/main/docs/linker/README.md)**\n\n```python\n# Initilize linkage components\nfrom gps_activity import ActivityLinkageSession\nfrom gps_activity.linker.factory import PreprocessingFactory\nfrom gps_activity.linker.factory import ClusterAggregationFactory\nfrom gps_activity.linker.factory import JoinValidatorFactory\nfrom gps_activity.linker.factory import SpatialJoinerFactory\nfrom gps_activity.linker.factory import CoverageStatisticsFactory\n\n\nMAX_DISTANCE = 100\nMAX_DAYS_DISTANCE = 1\n\n\ngps_link_preprocess_pipeline = PreprocessingFactory.factory_pipeline(\n    source_lat_column="lat",\n    source_lon_column="lon",\n    source_datetime="datetime",\n    source_vehicle_id="plate_no",\n    source_crs=WSG_84,\n    target_crs=HK_CRS,\n    generate_primary_key_for="gps",\n    source_composite_keys=["plate_no", "datetime", "lat", "lon"],\n)\n\nplans_link_preprocess_pipeline = PreprocessingFactory.factory_pipeline(\n    source_lat_column="lat",\n    source_lon_column="lng",\n    source_datetime="datetime",\n    source_vehicle_id="re-assigned by Ricky",\n    source_crs=WSG_84,\n    target_crs=HK_CRS,\n    generate_primary_key_for="plan",\n    source_composite_keys=["CRN#"],\n)\n\ncluster_agg_pipeline = ClusterAggregationFactory.factory_pipeline(\n    source_lat_column="lat",\n    source_lon_column="lon",\n    source_datetime="datetime",\n    source_vehicle_id="plate_no",\n    source_crs=WSG_84,\n    target_crs=HK_CRS,\n)\n\nspatial_joiner = SpatialJoinerFactory.factory_pipeline(how="inner", max_distance=MAX_DISTANCE)\nspatial_validator = JoinValidatorFactory.factory_pipeline(max_days_distance=MAX_DAYS_DISTANCE,\n                                                          ensure_vehicle_overlap=True)\ncoverage_stats_extractor = CoverageStatisticsFactory.factory_pipeline()\n\n\ngps_linker_session = ActivityLinkageSession(\n    gps_preprocessor=gps_link_preprocess_pipeline,\n    plan_preprocessor=plans_link_preprocess_pipeline,\n    cluster_aggregator=cluster_agg_pipeline,\n    spatial_joiner=spatial_joiner,\n    spatial_validator=spatial_validator,\n    coverage_stats_extractor=coverage_stats_extractor,\n)\n\n\nlinker_results = gps_linker_session.transform({\n    "gps": clustered_gps,\n    "plan": plans,\n})\n```\n\n## Metrics module implementation 📊\n\n* **NOTE**: This module is highly experimental\n* **NOTE**: This module depends on `linker` module\n\n```python\nfrom gps_activity.metrics import ActivityMetricsSession\nfrom gps_activity.metrics.models import Metrics\n\n\nmetrics = ActivityMetricsSession(beta=2)\nmetrics = metrics.transform(linker_results)\n```\n',
    'author': 'Adil Rashitov',
    'author_email': 'adil@wastelab.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
