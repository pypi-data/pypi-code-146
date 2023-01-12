# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zoish',
 'zoish.abstracs',
 'zoish.base_classes',
 'zoish.decorators',
 'zoish.examples',
 'zoish.examples.shap',
 'zoish.examples.single_feature',
 'zoish.factories',
 'zoish.feature_selectors',
 'zoish.mediators']

package_data = \
{'': ['*'],
 'zoish': ['logs/*'],
 'zoish.examples': ['recursive_addition_features/*',
                    'recursive_elimination_features/*',
                    'select_by_shuffling/*']}

install_requires = \
['catboost>=1.0.6,<2.0.0',
 'category-encoders>=2.5.0,<3.0.0',
 'click>=8.1.3,<9.0.0',
 'fasttreeshap>=0.1.2,<0.2.0',
 'feature-engine>=1.4.1,<2.0.0',
 'imblearn>=0.0,<0.1',
 'lightgbm>=3.3.2,<4.0.0',
 'lohrasb>=2.1.0,<3.0.0',
 'matplotlib>=3.5.2,<4.0.0',
 'numba>=0.55.2,<0.56.0',
 'numpy<1.63.0',
 'optuna>=2.10.1,<3.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pip-licenses>=3.5.4,<4.0.0',
 'pycox>=0.2.3,<0.3.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'scipy>=1.8.1,<2.0.0',
 'shap>=0.41.0,<0.42.0',
 'xgboost>=1.6.1,<2.0.0',
 'xgbse>=0.2.3,<0.3.0']

setup_kwargs = {
    'name': 'zoish',
    'version': '2.0.1',
    'description': 'This project uses shapely values for selecting Top n features compatible with scikit learn pipeline',
    'long_description': '# Zoish\n\nZoish is a package built to ease machine learning development by providing various feature-selecting modules such as:  \n- Select By Single Feature Performance\n- Recursive Feature Elimination\n- Recursive Feature Addition\n- Select By Shuffling\n\nAll of them are compatible with [scikit-learn](https://scikit-learn.org) pipeline. \n\n\n## Introduction\n\nAll of the above-mentioned modules of Zoish have class factories that have various methods and parameters. From an estimator to its tunning parameters and from optimizers to their parameters, the final goal is to automate the feature selection of the ML pipeline in a proper way. Optimizers like [Optuna](https://optuna.org/), [GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html) ,and [RandomizedSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RandomizedSearchCV.html) has critical role in Zoish. They are used to provide the best estimator on a train set that is later used by feature selectors to check what features can improve the accuracy of this best estimator based on desired metrics. In short, Optimizers use information every bit of information in rain set to select the best feature set. \n\nThe main process in Zoish is to split samples to train and validation set, and then optimization will estimate optimal hyper-parameters of the estimators. After that, this best estimator will be input to the feature selection objects and finally, the best subset of features with higher grades will be returned. This subset can be used as the next steps of the ML pipeline. In the next paragraphs, more details about feature selector modules have provided.\n\n### ShapFeatureSelectorFactory\n\nShapFeatureSelectorFactory uses  [SHAP](https://arxiv.org/abs/1705.07874) (SHapley Additive exPlanation)  for a better feature selection. This package uses [FastTreeSHAP](https://arxiv.org/abs/2109.09847) while calculating shap values and [SHAP](https://shap.readthedocs.io/en/latest/index.html) for plotting. Using this module users can : \n\n- find features using the best estimator of tree-based models with the highest shap values after hyper-parameter optimization.\n- draw some shap related plots for selected features.\n- return a  Pandas data frame with a list of features and shap values. \n\n### RecursiveFeatureEliminationFeatureSelectorFactory\n\nThe job of this factory class is to ease the selection of features by following a recursive elimination process. The process uses the best estimator found by the optimizer using all the features. Then it ranks the features according to their importance derived from the best estimator. In the next step, it removes the least important feature and fits again with the best estimator. It calculates the performance of the best estimator again and calculates the performance difference between the new and old results. If the performance drop is below the threshold the feature is removed, and this process will continue until all features have been evaluated. For more information on the logic of the recursive elimination process visit this [RecursiveFeatureElimination](https://feature-engine.readthedocs.io/en/latest/api_doc/selection/RecursiveFeatureElimination.html) page. \n\n### RecursiveFeatureAdditionFeatureSelectorFactory\nIt is very similar to RecursiveFeatureEliminationFeatureSelectorFactory, however, the logic is the opposite. It selects features following a recursive addition process. Visit [RecursiveFeatureAddition](https://feature-engine.readthedocs.io/en/latest/api_doc/selection/RecursiveFeatureAddition.html) for more details. \n\n### SelectByShufflingFeatureSelectorFactory\n\nIn this module, the selection of features is based on determining the drop in machine learning model performance when each feature’s values are randomly shuffled.\n\nIf the variables are important, a random permutation of their values will decrease dramatically the machine learning model performance. Contrarily, the permutation of the values should have little to no effect on the model performance metric we are assessing if the feature is not predictive. To understand how it works completely go to its official page [SelectByShuffling](https://feature-engine.readthedocs.io/en/latest/api_doc/selection/SelectByShuffling.html).\n\n### SingleFeaturePerformanceFeatureSelectorFactory\n\nIt selects features based on the performance of a machine learning model trained to utilize a single feature. In other words, it trains a machine-learning model for every single feature, then determines each model’s performance. If the performance of the model is greater than a user-specified threshold, then the feature is retained, otherwise removed. Go to this [page](https://feature-engine.readthedocs.io/en/latest/api_doc/selection/SelectBySingleFeaturePerformance.html) for more information. \n\n## Installation\n\nZoish package is available on PyPI and can be installed with pip:\n\n```sh\npip install zoish\n```\n\nFor log configuration in development environment use \n\n```sh\nexport env=dev\n\n```\n\nFor log configuration in production environment use \n\n```sh\nexport env=prod\n```\n\n## Examples \n\n### Import required libraries\n```\nfrom zoish.feature_selectors.shap_selectors import ShapFeatureSelector\nimport pandas as pd\nfrom sklearn.model_selection import train_test_split\nimport pandas as pd\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.metrics import r2_score\nfrom feature_engine.imputation import CategoricalImputer, MeanMedianImputer\nfrom category_encoders import OrdinalEncoder\nimport xgboost\nimport optuna\nfrom optuna.samplers import TPESampler\nfrom optuna.pruners import HyperbandPruner\nfrom sklearn.linear_model import LinearRegression\n```\n\n### Computer Hardware Data Set (a classification problem)\n```\nurldata= "https://archive.ics.uci.edu/ml/machine-learning-databases/cpu-performance/machine.data"\n# column names\ncol_names=[\n    "vendor name",\n    "Model Name",\n    "MYCT",\n    "MMIN",\n    "MMAX",\n    "CACH",\n    "CHMIN",\n    "CHMAX",\n    "PRP"\n]\n# read data\ndata = pd.read_csv(urldata,header=None,names=col_names,sep=\',\')\n\n```\n### Train test split\n```\nX = data.loc[:, data.columns != "PRP"]\ny = data.loc[:, data.columns == "PRP"]\n\nX_train, X_test, y_train, y_test =train_test_split(X, y, test_size=0.33, random_state=42)\n```\n### Find feature types for later use\n```\nint_cols =  X_train.select_dtypes(include=[\'int\']).columns.tolist()\nfloat_cols =  X_train.select_dtypes(include=[\'float\']).columns.tolist()\ncat_cols =  X_train.select_dtypes(include=[\'object\']).columns.tolist()\n```\n\n###  Define Feature selector and set its arguments  \n```\nshap_feature_selector_factory = (\n    ShapFeatureSelector.shap_feature_selector_factory.set_model_params(\n        X=X_train,\n        y=y_train,\n        verbose=10,\n        random_state=0,\n        estimator=xgboost.XGBRegressor(),\n        estimator_params={\n            "max_depth": [4, 5],\n        },\n        fit_params = {\n            "callbacks": None,\n        },\n        method="optuna",\n        # if n_features=None only the threshold will be considered as a cut-off of features grades.\n        # if threshold=None only n_features will be considered to select the top n features.\n        # if both of them are set to some values, the threshold has the priority for selecting features.\n        n_features=5,\n        threshold = None,\n        list_of_obligatory_features_that_must_be_in_model=[],\n        list_of_features_to_drop_before_any_selection=[],\n    )\n    .set_shap_params(\n        model_output="raw",\n        feature_perturbation="interventional",\n        algorithm="v2",\n        shap_n_jobs=-1,\n        memory_tolerance=-1,\n        feature_names=None,\n        approximate=False,\n        shortcut=False,\n    )\n    .set_optuna_params(\n            measure_of_accuracy="r2_score(y_true, y_pred)",\n            # optuna params\n            with_stratified=False,\n            test_size=.3,\n            n_jobs=-1,\n            # optuna params\n            # optuna study init params\n            study=optuna.create_study(\n                storage=None,\n                sampler=TPESampler(),\n                pruner=HyperbandPruner(),\n                study_name="example of optuna optimizer",\n                direction="maximize",\n                load_if_exists=False,\n                directions=None,\n            ),\n            # optuna optimization params\n            study_optimize_objective=None,\n            study_optimize_objective_n_trials=20,\n            study_optimize_objective_timeout=600,\n            study_optimize_n_jobs=-1,\n            study_optimize_catch=(),\n            study_optimize_callbacks=None,\n            study_optimize_gc_after_trial=False,\n            study_optimize_show_progress_bar=False,\n            )\n)\n\n```\n### Build sklearn Pipeline  \n```\npipeline =Pipeline([\n            # int missing values imputers\n            (\'intimputer\', MeanMedianImputer(\n                imputation_method=\'median\', variables=int_cols)),\n            # category missing values imputers\n            (\'catimputer\', CategoricalImputer(variables=cat_cols)),\n            #\n            (\'catencoder\', OrdinalEncoder()),\n            # feature selection\n            ("sfsf", shap_feature_selector_factory),\n            # add any regression model from sklearn e.g., LinearRegression\n            (\'regression\', LinearRegression())\n\n\n ])\n```\n### Run Pipeline\n```\npipeline.fit(X_train,y_train)\ny_pred = pipeline.predict(X_test)\n\n```\n### Plots\n```\nShapFeatureSelector.shap_feature_selector_factory.plot_features_all(\n    type_of_plot="summary_plot",\n    path_to_save_plot="../plots/shap_optuna_search_regression_summary_plot"\n)\n```\n\n###  Check performance of the Pipeline\n```\nprint(\'r2 score : \')\nprint(r2_score(y_test,y_pred))\n\n```\n### Get access to feature selector instance\n```\nprint(ShapFeatureSelector.shap_feature_selector_factory.get_feature_selector_instance())\n```\n\n\nMore examples are available in the [examples](https://github.com/drhosseinjavedani/zoish/tree/main/zoish/examples). \n\n## License\nLicensed under the [BSD 2-Clause](https://opensource.org/licenses/BSD-2-Clause) License.',
    'author': 'drhosseinjavedani',
    'author_email': 'h.javedani@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/drhosseinjavedani/zoish',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
