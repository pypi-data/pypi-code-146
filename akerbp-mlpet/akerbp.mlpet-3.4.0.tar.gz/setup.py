# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['akerbp',
 'akerbp.mlpet',
 'akerbp.mlpet.data',
 'akerbp.mlpet.tests',
 'akerbp.mlpet.tests.data']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1',
 'cognite-sdk>=4.4.3,<5.0.0',
 'importlib-metadata>=4.12.0,<5.0.0',
 'joblib>=1.0.1',
 'lasio>=0.29',
 'numpy>=1.19.5',
 'pandas>=1.3.2',
 'plotly>=5.8.2',
 'scikit-learn>=0.24.2',
 'scipy>=1.7.1',
 'tqdm>=4.62.3,<5.0.0']

extras_require = \
{'version': ['requests>=2.28.0,<3.0.0',
             'python-dateutil>=2.8.2,<3.0.0',
             'packaging>=21.3,<22.0']}

setup_kwargs = {
    'name': 'akerbp.mlpet',
    'version': '3.4.0',
    'description': 'Package to prepare well log data for ML projects.',
    'long_description': '# akerbp.mlpet\n\nPreprocessing tools for Petrophysics ML projects at Eureka\n\n## Installation\n\nInstall the package by running the following (requires python 3.8 or later)\n\n        pip install akerbp.mlpet\n\n\n## Quick start\n\nFor a short example of how to use the mlpet Dataset class for pre-processing data see below. Please refer to the tests folder of this repository for more examples as well as some examples of the `settings.yaml` file:\n\n        import os\n        from akerbp.mlpet import Dataset\n        from akerbp.mlpet import utilities\n\n        # Instantiate an empty dataset object using the example settings and mappings provided\n        ds = Dataset(\n                settings=os.path.abspath("settings.yaml"), # Absolute file paths are required\n                folder_path=os.path.abspath(r"./"), # Absolute file paths are required\n        )\n\n        # Populate the dataset with data from a file (support for multiple file formats and direct cdf data collection exists)\n        ds.load_from_pickle(r"data.pkl") # Absolute file paths are preferred\n\n        # The original data will be kept in ds.df_original and will remain unchanged\n        print(ds.df_original.head())\n\n        # Split the data into train-validation sets\n        df_train, df_test = utilities.train_test_split(\n                df=ds.df_original,\n                target_column=ds.label_column,\n                id_column=ds.id_column,\n                test_size=0.3,\n        )\n\n        # Preprocess the data for training according to default workflow\n        # print(ds.default_preprocessing_workflow) <- Uncomment to see what the workflow does\n        df_preprocessed = ds.preprocess(df_train)\n\n\nThe procedure will be exactly the same for any other dataset class. The only difference will be in the "settings". For a full list of possible settings keys see either the [built documentation](docs/build/html/akerbp.mlpet.html) or the akerbp.mlpet.Dataset class docstring. Make sure that the curve names are consistent with those in the dataset.\n\nThe loaded data is NOT mapped at load time but rather at preprocessing time (i.e. when preprocess is called).\n\n## Recommended workflow for preprocessing\n\nDue to the operations performed by certain preprocessing methods in akerbp.mlpet, the order in which the different preprocessing steps can sometimes be important for achieving the desired results. Below is a simple guide that should be followed for most use cases:\n1. Misrepresented missing data should always be handled first (using `set_as_nan`)\n2. This should then be followed by data cleaning methods (e.g. `remove_outliers`, `remove_noise`, `remove_small_negative_values`)\n3. Depending on your use case, once the data is clean you can then impute missing values (see `imputers.py`). Note however that some features depend on the presence of missing values to provide better estimates (e.g. `calculate_VSH`)\n4. Add new features (using methods from `feature_engineering.py`) or using `process_wells` from `preprocessors.py` if the features should be well specific.\n5. Fill missing values if any still exist or were created during step 4. (using `fillna_with_fillers`)\n6. Scale whichever features you want (using `scale_curves` from `preprocessors.py`). In some use cases this step could also come before step 5.\n7. Encode the GROUP & FORMATION column if you want to use it for training. (using `encode_columns` from `preprocessors.py`)\n8. Select or drop the specific features you want to keep for model training. (using `select_columns` or `drop_columns` from `preprocessors.py`)\n\n> **_NOTE:_**  The dataset class **drops** all input columns that are not explicitly named in your settings.yaml or settings dictionary passed to the Dataset class at instantiation. This is to ensure that the data is not polluted with features that are not used. Therefore, if you have features that are being loaded into the Dataset class but are not being preprocessed, these need to be explicitly defined in your settings.yaml or settings dictionary under the keyword argument `keep_columns`.\n\n## API Documentation\n\nFull API documentaion of the package can be found under the [docs](docs/build/html/index.html) folder once you have run the make html command.\n\n## For developers\n\n- to make the API documentation, from the root directory of the project run (assuming you have installed all development dependencies)\n\n        cd docs/\n        make html\n\n- to install mlpet in editable mode for use in another project, there are two\n  possible solutions dependent on the tools being used:\n   1. If the other package uses poetry, please refer to this [guide](https://github.com/python-poetry/poetry/discussions/1135#discussioncomment-145756)\n   2. If you are not using poetry (using conda, pyenv or something else), just revert to using `pip install -e .` from within the root directory (Note: you need to have pip version >= 21.3).\n## License\n\nakerbp.mlpet Copyright 2021 AkerBP ASA\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n',
    'author': 'Flavia Dias Casagrande',
    'author_email': 'flavia.dias.casagrande@akerbp.com',
    'maintainer': 'Yann Van Crombrugge',
    'maintainer_email': 'yann.vancrombrugge@akerbp.com',
    'url': 'https://bitbucket.org/akerbp/akerbp.mlpet/src/master/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
