# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aligned',
 'aligned.compiler',
 'aligned.data_source',
 'aligned.feature_view',
 'aligned.feature_view.tests',
 'aligned.jobs.tests',
 'aligned.local',
 'aligned.local.tests',
 'aligned.psql',
 'aligned.redis',
 'aligned.redis.tests',
 'aligned.redshift',
 'aligned.request',
 'aligned.request.tests',
 'aligned.s3',
 'aligned.schemas',
 'aligned.tests',
 'aligned.validation',
 'aligned.validation.tests']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'dill>=0.3.4,<0.4.0',
 'httpx>=0.23.0,<0.24.0',
 'mashumaro>=3.0.1,<4.0.0',
 'nest-asyncio>=1.5.5,<2.0.0',
 'pandas>=1.3.1,<2.0.0',
 'polars[all]>=0.15.6,<0.16.0',
 'pyarrow>=8.0.0,<9.0.0']

extras_require = \
{'aws': ['aioaws>=0.12,<0.13', 'databases>=0.5.5,<0.6.0'],
 'dask': ['dask[dataframe]>=2022.7.0,<2023.0.0'],
 'pandera': ['pandera>=0.13.3,<0.14.0'],
 'psql': ['databases>=0.5.5,<0.6.0', 'asyncpg>=0.25.0,<0.26.0'],
 'redis': ['redis>=4.3.1,<5.0.0'],
 'server': ['fastapi>=0.77.1,<0.78.0',
            'uvicorn>=0.17.6,<0.18.0',
            'asgi-correlation-id>=3.0.0,<4.0.0']}

entry_points = \
{'console_scripts': ['aligned = aligned.cli:cli']}

setup_kwargs = {
    'name': 'aligned',
    'version': '0.0.10a0',
    'description': 'A scalable feature store that makes it easy to align offline and online ML systems',
    'long_description': '# Aligned\n\nAligned help defining a single source of truth for logic while keeping the technology stack flexible. Such innovation has been possible by removing the need to depend on a processing engine, leading to less- and more transparent- code. Furthermore, the declarative API has made it possible to comment, add data validation, and define feature transformation at the same location. Therefore, it leads to a precise definition of the intended result.\n\nMain advantages:\n- Test new features faster\n- Adapt faster to new technical and business requirements.\n- Stop technology lock-in, like processing engines and infrastructure.\n- Stop vendor lock-in. Deploy to any provider that fits you\n\nAs a result, loading model featurs can be done with the following code.\n\n```python\nawait store.model("titanic").features_for(entities).as_pandas()\n```\n\nRead the post about [how the most elegant MLOps tool was created](https://matsmoll.github.io/2022/12/31/How-I-created-the-most-elegant-MLOps-tool.html)\n\nAlso check out the the [example repo](https://github.com/otovo/aligned-example) to see how it can be used\n\nAligned is still in actice development, so changes are likely.\n\n## Feature Views\n\nWrite features as the should be, as data models.\nThen get code completion and typesafety by referencing them in other features.\n\nThis makes the features light weight, data source indipendent, and flexible.\n\n```python\nclass TitanicPassenger(FeatureView):\n\n    metadata = FeatureViewMetadata(\n        name="passenger",\n        description="Some features from the titanic dataset",\n        batch_source=FileSource.csv_at("titanic.csv"),\n        stream_source=HttpStreamSource(topic_name="titanic")\n    )\n\n    passenger_id = Entity(dtype=Int32())\n\n    # Input values\n    age = (\n        Float()\n            .description("A float as some have decimals")\n            .is_required()\n            .lower_bound(0)\n            .upper_bound(110)\n    )\n\n    name = String()\n    sex = String().accepted_values(["male", "female"])\n    survived = Bool().description("If the passenger survived")\n    sibsp = Int32().lower_bound(0, is_inclusive=True).description("Number of siblings on titanic")\n    cabin = String()\n\n    # Creates two one hot encoded values\n    is_male, is_female = sex.one_hot_encode([\'male\', \'female\'])\n\n    # Standard scale the age.\n    # This will fit the scaler using a data slice from the batch source\n    # limited to maximum 100 rows. We can also uese a time constraint if wanted\n    scaled_age = age.standard_scaled(limit=100)\n```\n\n## Data sources\n\nAlinged makes handling data sources easy, as you do not have to think about how it is done.\nOnly define where the data is, and we handle the dirty work.\n\n```python\nmy_db = PostgreSQLConfig(env_var="DATABASE_URL")\n\nclass TitanicPassenger(FeatureView):\n\n    metadata = FeatureViewMetadata(\n        name="passenger",\n        description="Some features from the titanic dataset",\n        batch_source=my_db.table(\n            "passenger",\n            mapping_keys={\n                "Passenger_Id": "passenger_id"\n            }\n        ),\n        stream_source=HttpStreamSource(topic_name="titanic")\n    )\n\n    passenger_id = Entity(dtype=Int32())\n```\n\n### Fast development\n\nMaking iterativ and fast exploration in ML is important. This is why Aligned also makes it super easy to combine, and test multiple sources.\n\n```python\nmy_db = PostgreSQLConfig.localhost()\n\naws_bucket = AwsS3Config(...)\n\nclass SomeFeatures(FeatureView):\n\n    metadata = FeatureViewMetadata(\n        name="some_features",\n        description="...",\n        batch_source=my_db.table("local_features")\n    )\n\n    # Some features\n    ...\n\nclass AwsFeatures(FeatureView):\n\n    metadata = FeatureViewMetadata(\n        name="aws",\n        description="...",\n        batch_source=aws_bucket.file_at("path/to/file.parquet")\n    )\n\n    # Some features\n    ...\n```\n\n## Model Service\n\nUsually will you need to combine multiple features for each model.\nThis is where a `ModelService` comes in.\nHere can you define which features should be exposed.\n\n```python\n# Uses the variable name, as the model service name.\n# Can also define a custom name, if wanted.\ntitanic_model = ModelService(\n    features=[\n        TitanicPassenger.select_all(),\n\n        # Select features with code completion\n        LocationFeatures.select(lambda view: [\n            view.distance_to_shore,\n            view.distance_to_closest_boat\n        ]),\n    ]\n)\n```\n\n\n## Data Enrichers\n\nIn manny cases will extra data be needed in order to generate some features.\nWe therefore need some way of enriching the data.\nThis can easily be done with Alinged\'s `DataEnricher`s.\n\n```python\nmy_db = PostgreSQLConfig.localhost()\nredis = RedisConfig.localhost()\n\nuser_location = my_db.data_enricher( # Fetch all user locations\n    sql="SELECT * FROM user_location"\n).cache( # Cache them for one day\n    ttl=timedelta(days=1),\n    cache_key="user_location_cache"\n).lock( # Make sure only one processer fetches the data at a time\n    lock_name="user_location_lock",\n    redis_config=redis\n)\n\n\nasync def distance_to_users(df: DataFrame) -> Series:\n    user_location_df = await user_location.load()\n    ...\n    return distances\n\nclass SomeFeatures(FeatureView):\n\n    metadata = FeatureViewMetadata(...)\n\n    latitude = Float()\n    longitude = Float()\n\n    distance_to_users = Float().transformed(distance_to_users, using_features=[latitude, longitude])\n```\n\n\n## Access Data\n\nYou can easily create a feature store that contains all your feature definitions.\nThis can then be used to genreate data sets, setup an instce to serve features, DAG\'s etc.\n\n```python\nstore = FeatureStore.from_dir(".")\n\n# Select all features from a single feature view\ndf = await store.all_for("passenger", limit=100).to_df()\n```\n\n### Centraliced Feature Store Definition\nYou would often share the features with other coworkers, or split them into different stages, like `staging`, `shadow`, or `production`.\nOne option is therefore to reference the storage you use, and load the `FeatureStore` from there.\n\n```python\naws_bucket = AwsS3Config(...)\nstore = await aws_bucket.file_at("production.json").feature_store()\n\n# This switches from the production online store to the offline store\n# Aka. the batch sources defined on the feature views\nexperimental_store = store.offline_store()\n```\nThis json file can be generated by running `alinged apply`.\n\n### Select multiple feature views\n\n```python\ndf = await store.features_for({\n    "passenger_id": [1, 50, 110]\n}, features=[\n    "passenger:scaled_age",\n    "passenger:is_male",\n    "passenger:sibsp"\n\n    "other_features:distance_to_closest_boat",\n]).to_df()\n```\n\n### Model Service\n\nSelecting features for a model is super simple.\n\n\n```python\ndf = await store.model("titanic_model").features_for({\n    "passenger_id": [1, 50, 110]\n}).to_df()\n```\n\n### Feature View\n\nIf you want to only select features for a specific feature view, then this is also possible.\n\n```python\nprev_30_days = await store.feature_view("match").previous(days=30).to_df()\nsample_of_20 = await store.feature_view("match").all(limit=20).to_df()\n```\n\n## Data quality\nAlinged will make sure all the different features gets formatted as the correct datatype.\nIn addition will aligned also make sure that the returend features aligne with defined constraints.\n\n```python\nclass TitanicPassenger(FeatureView):\n\n    ...\n\n    age = (\n        Float()\n            .is_required()\n            .lower_bound(0)\n            .upper_bound(110)\n    )\n    sibsp = Int32().lower_bound(0, is_inclusive=True)\n```\n\nThen since our feature view have a `is_required` and a `lower_bound`, will the `.validate(...)` command filter out the entites that do not follow that behavior.\n\n```python\nfrom aligned.validation.pandera import PanderaValidator\n\ndf = await store.model("titanic_model").features_for({\n    "passenger_id": [1, 50, 110]\n}).validate(\n    PanderaValidator()  # Validates all features\n).to_df()\n```\n\n## Feature Server\n\nThis expectes that you either run the command in your feature store repo, or have a file with a `RepoReference` instance.\nYou can also setup an online source like Redis, for faster storage.\n\n```python\nredis = RedisConfig.localhost()\n\naws_bucket = AwsS3Config(...)\n\nrepo_files = RepoReference(\n    env_var_name="ENVIRONMENT",\n    repo_paths={\n        "production": aws_bucket.file_at("feature-store/production.json"),\n        "shadow": aws_bucket.file_at("feature-store/shadow.json"),\n        "staging": aws_bucket.file_at("feature-store/staging.json")\n        # else generate the feature store from the current dir\n    }\n)\n\n# Use redis as the online source, if not running localy\nif repo_files.selected != "local":\n    online_source = redis.online_source()\n```\n\nThen run `aligned serve`, and a FastAPI server will start. Here can you push new features, which then transforms and stores the features, or just fetch them.\n',
    'author': 'Mats E. Mollestad',
    'author_email': 'mats@mollestad.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/otovo/aladdin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
