from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
import logging
import os
import shutil
import tempfile
from typing import Any, List, Mapping, Optional, Sequence

import cloudpickle
import sklearn

from truera.client.errors import InvalidFrameworkWrapperException
from truera.client.model_preprocessing import BUILT_IN_FRAMEWORK_WRAPPER_MAP
from truera.client.model_preprocessing import create_temp_file_path
from truera.client.model_preprocessing import get_module_version
from truera.client.model_preprocessing import ModelFile
from truera.client.model_preprocessing import PipDependencyParser
from truera.client.model_preprocessing import prepare_python_model_folder
from truera.client.util.lightgbm_classification_predict_wrapper import \
    validate_lightgbm_booster_classifier
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION  # pylint: disable=no-name-in-module
from truera.protobuf.public.metadata_message_types_pb2 import \
    FeatureTransformationType  # pylint: disable=no-name-in-module
from truera.utils.pyspark_util import is_supported_pyspark_tree_model


@dataclass
class ModuleInfo:
    required_dependencies: list()
    install_name: str = ""


# Devnote: since this is hard-coded by engineers, we should be careful to avoid cyclic dpeendencies
DEPENDENCY_MAP: Mapping[str, ModuleInfo] = {
    'xgboost': ModuleInfo(['sklearn', 'xgboost'], 'xgboost'),
    'sklearn': ModuleInfo(['sklearn'], 'scikit-learn'),
    'sklearn_pipeline': ModuleInfo(['sklearn'], 'scikit-learn'),
    'catboost': ModuleInfo(['catboost'], 'catboost'),
    'lightgbm': ModuleInfo(['lightgbm'], 'lightgbm'),
    'pyspark': ModuleInfo(['pyspark'], 'pyspark')
}


class PythonModelPackager(ABC):

    def __init__(
        self, model: Any, transformer: Optional[Any], model_output_type: str,
        python_version: str, additional_pip_dependencies: PipDependencyParser
    ) -> None:
        self.model = model
        self.transformer = transformer
        self.model_output_type = model_output_type
        self.python_version = python_version
        self.model_module = ""
        self.additional_pip_dependencies = additional_pip_dependencies
        self.dependency_map = DEPENDENCY_MAP.copy()

    #TODO(AB#6983): The save method should be further refactored for the child classes.

    @abstractmethod
    def save_model(
        self,
        logger: logging.Logger,
        output_dir: str,
        *,
        additional_modules: Optional[Sequence[Any]] = None
    ):
        """Packages and save the model after running validation and resolving outstanding dependencies. 

        Args:
            logger: Logger object.
            output_dir: Destination directory to save the model after packaging.
            additional_modules: List of modules not available as pip packages required for the model. These must already be imported. Defaults to None.
        """
        pass

    @abstractmethod
    def resolve_pip_dependencies(self, logger: logging.Logger):
        """Resolves any outstanding dependencies. For known model types, it checks for required dependencies in `additional_pip_dependencies` or infers it from current environment and sets it.
        Raises:
            ValueError: if version cannot be determined for any required package.
        """
        pass

    def _pickle_with_additional_modules(
        self,
        obj: Any,
        file_name: str,
        additional_modules: Optional[Sequence[Any]] = None,
    ):
        with open(file_name, "wb") as f:
            if additional_modules is None:
                additional_modules = []
            try:
                for curr in additional_modules:
                    cloudpickle.register_pickle_by_value(curr)
                cloudpickle.dump(obj, f)
            finally:
                for curr in additional_modules:
                    try:
                        cloudpickle.unregister_pickle_by_value(curr)
                    except:
                        pass

    def _dump_pickle_and_save_model(
        self,
        logger: logging.Logger,
        output_dir: str,
        framework_wrapper: str,
        model_code_files: Optional[List[ModelFile]] = None,
        additional_modules: Optional[Sequence[Any]] = None
    ):
        """Creates and saves the pickle file for model along with all additional dependencies and configuration.

        Args:
            logger: Logger object
            output_dir: Destination dictory for saving the model.
            framework_wrapper: Framework for the model.
            model_code_files: Additional model code files. Defaults to None.
            additional_modules: List of modules not available as pip packages required for the model. These must already be imported.. Defaults to None.
        """
        self._validate_transform_support(framework_wrapper)
        logger.debug("Saving model as pickle file.")
        pickle_file_temp_location = create_temp_file_path()
        self._pickle_with_additional_modules(
            self.model, pickle_file_temp_location, additional_modules
        )
        transform_pickle_file_temp_location = None
        if self.transformer is not None:
            transform_pickle_file_temp_location = create_temp_file_path()
            self._pickle_with_additional_modules(
                self.transformer, transform_pickle_file_temp_location,
                additional_modules
            )
        if model_code_files is None:
            model_code_files = []
        try:
            logger.debug(f"Packaged model path: {output_dir}")
            prepare_python_model_folder(
                pickle_file_temp_location,
                output_dir,
                framework_wrapper=framework_wrapper,
                model_output_type=self.model_output_type,
                pip_dependencies=self.additional_pip_dependencies,
                python_version=self.python_version,
                pip_version=self.get_pip_version(),
                conda_file=None,
                dependencies=None,
                model_code_files=model_code_files,
                logger=logger,
                transform_file_path=transform_pickle_file_temp_location
            )
        finally:
            try:
                os.remove(pickle_file_temp_location)
                if self.transformer is not None:
                    os.remove(transform_pickle_file_temp_location)
            except:
                pass

    def get_module_version_from_current_env(self,
                                            pkg_name: str) -> Optional[str]:
        """Gets the version for a python package from current environment.

        Args:
            pkg_name: Name of the python package we want the version for.
        Returns:
            str: Version if available or None.
        """
        return get_module_version(pkg_name)

    def get_pip_version(self) -> Optional[str]:
        return self.get_module_version_from_current_env("pip")

    def check_or_set_module_versions_for_all_dependencies(
        self, logger: logging.Logger, module: Optional[str] = None
    ):
        """Checks if all required dependencies for a python model type is present in the `additional_pip_dependencies`.
        If any required dependency is missing, it tries to set it from current environment.

        Raises:
            ValueError: if version cannot be determined for any required dependency. We do not want to add unbounded package.
        """
        if not module:
            module = self.model_module
        dependency_info = self.dependency_map.get(module)
        if dependency_info:
            for dependency in dependency_info.required_dependencies:
                existing_dependencies = self.additional_pip_dependencies.get_package_names(
                )
                dep_info_for_dependency = self.dependency_map.get(dependency)
                if not dep_info_for_dependency:
                    raise ValueError(
                        f"Cannot resolve correctly: {dependency}. Pass it in `additional_pip_dependencies`."
                    )
                if dep_info_for_dependency.install_name not in existing_dependencies:
                    dependency_version = self.get_module_version_from_current_env(
                        self.dependency_map.get(dependency).install_name or
                        dependency
                    )
                    if dependency_version:
                        self.additional_pip_dependencies.add_dependency(
                            self.dependency_map.get(dependency).install_name or
                            dependency, dependency_version
                        )
                    else:
                        raise ValueError(
                            f"Version cannot be determined for a required dependency: {dependency}. Pass it in `additional_pip_dependencies`."
                        )
        else:
            logger.warning(
                f"Dependency info missing in the dependency map for {module}"
            )

    def _validate_transform_support(self, framework_wrapper: str):
        if not BUILT_IN_FRAMEWORK_WRAPPER_MAP[
            framework_wrapper.lower()].supports_transform and self.transformer:
            message = "Transform function or object not supported for this model type"
            raise InvalidFrameworkWrapperException(message)


class XgBoostModelPackager(PythonModelPackager):

    def __init__(
        self, model: Any, transformer: Optional[Any], model_output_type: str,
        python_version: str, additional_pip_dependencies: PipDependencyParser
    ) -> None:
        super().__init__(
            model, transformer, model_output_type, python_version,
            additional_pip_dependencies
        )
        self.model_module = "xgboost"

    def resolve_pip_dependencies(self, logger: logging.Logger):
        return self.check_or_set_module_versions_for_all_dependencies(logger)

    def save_model(
        self,
        logger: logging.Logger,
        output_dir: str,
        *,
        additional_modules: Optional[Sequence[Any]] = None
    ):
        self.resolve_pip_dependencies(logger)
        logger.debug("Saving classifier as pickle file.")

        self._dump_pickle_and_save_model(
            logger,
            output_dir,
            framework_wrapper=self.model_module,
            additional_modules=additional_modules
        )


class SklearnPipelineModelPackager(PythonModelPackager):

    def __init__(
        self,
        model: sklearn.pipeline.Pipeline,
        transformer: Optional[Any],
        model_output_type: str,
        python_version: str,
        additional_pip_dependencies: PipDependencyParser,
        feature_transform_type:
        FeatureTransformationType = FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION
    ) -> None:
        super().__init__(
            model, transformer, model_output_type, python_version,
            additional_pip_dependencies
        )
        self.model_module = "sklearn_pipeline"
        self.feature_transform_type = feature_transform_type

    def resolve_pip_dependencies(self, logger: logging.Logger):
        for intermediate_model in self.model.named_steps:
            self.module_package_mapping(
                self.model.named_steps[intermediate_model], logger
            )

    def module_package_mapping(
        self, model: sklearn.pipeline.Pipeline, logger: logging.Logger
    ):
        (name, module) = (model.__class__.__name__, model.__class__.__module__)
        if module.startswith("xgboost"):
            self.model_module = "sklearn_pipeline_xgb"
            return self.check_or_set_module_versions_for_all_dependencies(
                logger, module="xgboost"
            )
        elif module.startswith("sklearn"):
            return self.check_or_set_module_versions_for_all_dependencies(
                logger, module="sklearn"
            )
        elif module == "catboost.core":
            return self.check_or_set_module_versions_for_all_dependencies(
                logger, module="catboost"
            )
        elif module.startswith("lightgbm"):
            LightGBMModelPackager(
                model, None, self.model_output_type, self.python_version,
                self.additional_pip_dependencies
            ).validate_lgbm_model(module, name)
            return self.check_or_set_module_versions_for_all_dependencies(
                logger, module="lightgbm"
            )
        elif is_supported_pyspark_tree_model(model):
            return self.check_or_set_module_versions_for_all_dependencies(
                logger, module="pyspark"
            )

    def _split_pipeline_object(self):
        if len(self.model.named_steps) > 1:
            self.transformer = self.model[:-1]
            self.model = self.model[-1]

    def save_model(
        self,
        logger: logging.Logger,
        output_dir: str,
        *,
        additional_modules: Optional[Sequence[Any]] = None
    ):
        self.validate_sklearn_model()
        self.resolve_pip_dependencies(logger)
        framework_wrapper = self.model_module
        if self.feature_transform_type == FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION:
            logger.info(
                "Assuming transforms in the pipeline match the one-to-many feature map added to the data collection, splitting transform and estimator."
            )
            self._split_pipeline_object()
        else:
            logger.info(
                "Feature map has not been added, ingesting pipeline as single model without splitting transform and estimator."
            )
            framework_wrapper = "sklearn"
        logger.debug("Saving model as pickle file.")

        self._dump_pickle_and_save_model(
            logger,
            output_dir,
            framework_wrapper=framework_wrapper,
            additional_modules=additional_modules
        )

    def validate_sklearn_model(self):
        if self.model_output_type == "classification":
            if not hasattr(self.model, "predict_proba"):
                raise ValueError(
                    "The object provided for the classification model does not contain a "
                    "`predict_proba` method. Make sure this is a supported \"classification\" model. "
                    "If this is a regression model, please provide the model_output_type=\"regression\". "
                    "See https://scikit-learn.org/stable/developers/develop.html for more details."
                )
        if self.model_output_type == "regression":
            if hasattr(self.model,
                       "predict_proba") or not hasattr(self.model, "predict"):
                raise ValueError(
                    "The object provided for the regression model contains a "
                    "`predict_proba` method or does not contain the `predict`. "
                    "Make sure this is a supported \"regression\" model. "
                    "If this is a classification model, please provide the model_output_type=\"classification\". "
                    "See https://scikit-learn.org/stable/developers/develop.html for more details."
                )


class SklearnModelPackager(PythonModelPackager):

    def __init__(
        self, model: Any, transformer: Optional[Any], model_output_type: str,
        python_version: str, additional_pip_dependencies: PipDependencyParser
    ) -> None:
        super().__init__(
            model, transformer, model_output_type, python_version,
            additional_pip_dependencies
        )
        self.model_module = "sklearn"

    def resolve_pip_dependencies(self, logger: logging.Logger):
        return self.check_or_set_module_versions_for_all_dependencies(logger)

    def save_model(
        self,
        logger: logging.Logger,
        output_dir: str,
        *,
        additional_modules: Optional[Sequence[Any]] = None
    ):
        self.validate_sklearn_model()
        self.resolve_pip_dependencies(logger)
        logger.debug("Saving model as pickle file.")

        self._dump_pickle_and_save_model(
            logger,
            output_dir,
            framework_wrapper=self.model_module,
            additional_modules=additional_modules,
        )

    def validate_sklearn_model(self):
        if self.model_output_type == "classification":
            if not hasattr(self.model, "predict_proba"):
                raise ValueError(
                    "The object provided for the classification model does not contain a "
                    "`predict_proba` method. Make sure this is a supported \"classification\" model. "
                    "If this is a regression model, please provide the model_output_type=\"regression\". "
                    "See https://scikit-learn.org/stable/developers/develop.html for more details."
                )
        if self.model_output_type == "regression":
            if hasattr(self.model,
                       "predict_proba") or not hasattr(self.model, "predict"):
                raise ValueError(
                    "The object provided for the regression model contains a "
                    "`predict_proba` method or does not contain the `predict`. "
                    "Make sure this is a supported \"regression\" model. "
                    "If this is a classification model, please provide the model_output_type=\"classification\". "
                    "See https://scikit-learn.org/stable/developers/develop.html for more details."
                )


class LightGBMModelPackager(PythonModelPackager):

    def __init__(
        self, model: Any, transformer: Optional[Any], model_output_type: str,
        python_version: str, additional_pip_dependencies: PipDependencyParser
    ) -> None:
        super().__init__(
            model, transformer, model_output_type, python_version,
            additional_pip_dependencies
        )
        self.model_module = "lightgbm"

    def resolve_pip_dependencies(self, logger: logging.Logger):
        return self.check_or_set_module_versions_for_all_dependencies(logger)

    def save_model(
        self,
        logger: logging.Logger,
        output_dir: str,
        *,
        additional_modules: Optional[Sequence[Any]] = None
    ):
        self.resolve_pip_dependencies(logger)
        logger.debug("Saving lightgbm model as pickle file.")
        import lightgbm
        if self.model_output_type == "classification" and isinstance(
            self.model, lightgbm.Booster
        ):
            validate_lightgbm_booster_classifier(self.model)
        self._dump_pickle_and_save_model(
            logger,
            output_dir,
            framework_wrapper=self.model_module,
            additional_modules=additional_modules
        )

    def validate_lgbm_model(self, module: str, name: str):
        if module == "lightgbm.basic" and name == "Booster":
            pass
        elif module == "lightgbm.sklearn" and name == "LGBMClassifier":
            if self.model_output_type != "classification":
                raise ValueError(
                    f"LGBMClassifier expected for classification model, found {self.model_output_type}."
                )
        elif module == "lightgbm.sklearn" and name == "LGBMRegressor":
            if self.model_output_type != "regression":
                raise ValueError(
                    f"LGBMRegressor expected for regression model, found {self.model_output_type}."
                )


class CatBoostModelPackager(PythonModelPackager):

    def __init__(
        self, model: Any, transformer: Optional[Any], model_output_type: str,
        python_version: str, additional_pip_dependencies: PipDependencyParser
    ) -> None:
        super().__init__(
            model, transformer, model_output_type, python_version,
            additional_pip_dependencies
        )
        self.model_module = "catboost"

    def resolve_pip_dependencies(self, logger: logging.Logger):
        return self.check_or_set_module_versions_for_all_dependencies(logger)

    def save_model(
        self,
        logger: logging.Logger,
        output_dir: str,
        *,
        additional_modules: Optional[Sequence[Any]] = None,
    ):
        self._validate_transform_support(self.model_module)
        self.resolve_pip_dependencies(logger)
        logger.debug("Saving model as catboost model")
        model_file_temp_location = create_temp_file_path(extension="cbm")
        try:
            self.model.save_model(model_file_temp_location, format="cbm")
            logger.debug(
                f"Output model file to temp path: {model_file_temp_location}"
            )
            logger.debug(f"Output staging directory {output_dir}")
            prepare_python_model_folder(
                model_file_temp_location,
                output_dir,
                framework_wrapper=self.model_module,
                model_output_type=self.model_output_type,
                python_version=self.python_version,
                pip_version=self.get_pip_version(),
                pip_dependencies=self.additional_pip_dependencies,
                model_data_file_name="model.cbm",
                conda_file=None,
                dependencies=None,
                logger=logger
            )
        finally:
            try:
                os.remove(model_file_temp_location)
            except:
                pass


class PySparkModelPackager(PythonModelPackager):

    def __init__(
        self, model: Any, transformer: Optional[Any], model_output_type: str,
        python_version: str, additional_pip_dependencies: PipDependencyParser
    ) -> None:
        super().__init__(
            model, transformer, model_output_type, python_version,
            additional_pip_dependencies
        )
        self.model_module = "pyspark"

    def resolve_pip_dependencies(self, logger: logging.Logger):
        return self.check_or_set_module_versions_for_all_dependencies(logger)

    def save_model(
        self,
        logger: logging.Logger,
        output_dir: str,
        *,
        additional_modules: Optional[Sequence[Any]] = None,
    ):
        """Upload Pyspark tree model to Truera deployment.
        Supported Pyspark Models:
            - GBTClassificationModel and GBTRegressionModel
            - RandomForestClassificationModel and RandomForestRegressionModel
            - DecisionTreeClassificationModel and DecisionTreeRegressionModel
        """
        self._validate_transform_support(self.model_module)
        self.resolve_pip_dependencies(logger)
        logger.debug("Saving model as pyspark model")
        temp_pyspark_model_dir = tempfile.mkdtemp()
        shutil.rmtree(temp_pyspark_model_dir, ignore_errors=True)
        try:
            self.model.save(path=temp_pyspark_model_dir)
            logger.debug(f"Model saved to temp path {temp_pyspark_model_dir}")
            logger.debug(f"Output staging directory {output_dir}")
            prepare_python_model_folder(
                temp_pyspark_model_dir,
                output_dir,
                framework_wrapper=self.model_module,
                model_output_type=self.model_output_type,
                python_version=self.python_version,
                pip_dependencies=self.additional_pip_dependencies,
                pip_version=self.get_pip_version(),
                model_data_file_name=None,
                conda_file=None,
                dependencies=None,
                logger=logger
            )
        finally:
            shutil.rmtree(temp_pyspark_model_dir, ignore_errors=True)


class ModelPredictPackager(PythonModelPackager):

    def __init__(
        self, model: Any, transformer: Optional[Any], model_output_type: str,
        python_version: str, additional_pip_dependencies: PipDependencyParser
    ) -> None:
        super().__init__(
            model, transformer, model_output_type, python_version,
            additional_pip_dependencies
        )
        self.model_module = "truera_pred_func"

    def resolve_pip_dependencies(self, logger: logging.Logger):
        return None

    def save_model(
        self,
        logger: logging.Logger,
        output_dir: str,
        *,
        additional_modules: Optional[Sequence[Any]] = None,
    ):
        logger.debug("Saving model as pickle file.")
        parent_dir = os.path.dirname(
            os.path.dirname(os.path.realpath(__file__))
        )
        truera_model_file = os.path.join(
            parent_dir, "intelligence", "truera_model.py"
        )
        return self._dump_pickle_and_save_model(
            logger,
            output_dir,
            framework_wrapper=self.model_module,
            additional_modules=additional_modules,
            model_code_files=[
                ModelFile(truera_model_file, "truera/client/intelligence")
            ]
        )
