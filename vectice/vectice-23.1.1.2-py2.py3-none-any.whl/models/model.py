from __future__ import annotations

import logging
import pickle  # nosec
from typing import Any

from vectice.models import Metric, Property

_logger = logging.getLogger(__name__)


class Model:
    """Represent a wrapped model.

    Iteration steps that represent models require a wrapped model.
    Wrapped models present Vectice with a learned predictor and
    appropriate metadata about that predictor in order to summarize
    the model in views of the iteration.

    """

    def __init__(
        self,
        library: str,
        technique: str,
        metrics: dict[str, int] | list[Metric] | Metric | None = None,
        properties: dict[str, str] | dict[str, int] | list[Property] | Property | None = None,
        name: str | None = None,
        attachments: str | list[str] | None = None,
        predictor: Any = None,
        capture_code: bool = True,
        inputs: list[int] | None = None,
    ):
        """Wrap a model (predictor).

        A Vectice Model is a wrapped predictor suitable for assignment
        to a Vectice Step.

        :param library: The library used to generate the model.
        :param technique: The modeling technique used.
        :param metrics: a dict for example {"MSE": 1}.
        :param properties: a dict, for example {"folds": 32}.
        :param name: The model name. If None, will be auto-generated based on the library and technique.
        :param attachments: Path of a file that will be attached to the step along with the predictor.
        :param capture_code: If True, automatically capture the current git commit hash if available.
        :param inputs: List of dataset version ids to link as lineage.

        """
        self._library = library
        self._technique = technique
        self._name = name if name else self._generate_name()
        self._metrics = self._format_metrics(metrics) if metrics else None
        self._properties = self._format_properties(properties) if properties else None
        self._attachments = self._format_attachments(attachments) if attachments else None
        self._capture_code = capture_code
        self._predictor = pickle.dumps(predictor)  # nosec
        self._inputs = inputs

    def __repr__(self):
        return (
            f"Model(name='{self.name}', library='{self.library}', technique='{self.technique}', "
            f"metrics={self.metrics}, properties={self.properties}, attachments={self.attachments})"
        )

    @property
    def name(self) -> str:
        """Return the model's name.

        :return: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Set the model's name.

        :param name: the name for the model
        """
        self._name = name

    @property
    def predictor(self) -> Any:
        """Return the predictor.

        :return: Any
        """
        return pickle.loads(self._predictor)  # nosec

    @predictor.setter
    def predictor(self, predictor: Any):
        """Set the predictor.

        :param predictor: the predictor

        """
        self._predictor = pickle.dumps(predictor)  # nosec

    @classmethod
    def read_predictor_file(cls, path: str) -> Any:
        return pickle.load(open(path, "rb"))  # nosec

    @property
    def library(self) -> str:
        """Return the name of the library used to generate the model.

        :return: str
        """
        return self._library

    @library.setter
    def library(self, library):
        """Set the name of the library used to create the model.

        :param library: the library used to create the model.
        """
        self._library = library

    @property
    def technique(self) -> str:
        """Return the name of the modeling technique used to learn the model.

        :return: str
        """
        return self._technique

    @technique.setter
    def technique(self, technique):
        """Set the name of the modeling technique used to learn the model.

        :param technique: the modeling technique used
        """
        self._technique = technique

    @property
    def metrics(self) -> list[Metric] | None:
        """Return the model's metrics.

        :return: Optional[List[Metric]]
        """
        return self._metrics

    @metrics.setter
    def metrics(self, metrics: dict[str, int] | list[Metric] | Metric | None):
        """Set the model's metrics.

        :param metrics: the metrics of the model
        """
        self._format_metrics(metrics)

    @property
    def properties(self) -> list[Property] | None:
        """Return the model's properties.

        :return: Optional[List[Property]]
        """
        return self._properties

    @properties.setter
    def properties(self, properties: dict[str, str] | list[Property] | Property | None):
        """Set the model's properties.

        :param properties: the properties of the model
        """
        self._format_properties(properties)

    @property
    def attachments(self) -> list[str] | None:
        """Return the attachments associated with the model.

        :return: Optional[List[str]]
        """
        return self._attachments

    @attachments.setter
    def attachments(self, attachments: list[str] | str):
        """Attach a file or files to the model.

        :param attachments: the filename or filenames of the file or set of files to attach to the model
        """
        self._attachments = self._format_attachments(attachments)

    @property
    def capture_code(self) -> bool:
        """Return whether or not to capture git commit at model assignment.

        If True and the current directory is managed by git, capture
        the SHA1 of the current commit and associate it with the model
        when the model is assigned.  If False, do not look for git
        data at model assignment time.

        :return: CodeSource

        """
        return self._capture_code

    @property
    def inputs(self) -> Any:
        """Return model inputs.

        :return: Any
        """
        return self._inputs

    def _generate_name(self) -> str:
        return f"{self.library} {self.technique} model"

    def _format_metrics(self, metrics: dict[str, int] | list[Metric] | Metric | None) -> list[Metric]:
        if metrics is None:
            return []
        if isinstance(metrics, Metric):
            return [metrics]
        if isinstance(metrics, list):
            metrics = self._remove_incorrect_metrics(metrics)
            key_list = [metric.key for metric in metrics]
            self._check_key_duplicates(key_list)
            return metrics
        if isinstance(metrics, dict):
            return [Metric(key, value) for (key, value) in metrics.items()]
        else:
            raise ValueError("Please check metric type.")

    @staticmethod
    def _check_key_duplicates(key_list: list[str]):
        if len(key_list) != len(set(key_list)):
            raise ValueError("Duplicate keys are not allowed.")

    @staticmethod
    def _remove_incorrect_metrics(metrics: list[Metric]) -> list[Metric]:
        for metric in metrics:
            if not isinstance(metric, Metric):
                logging.warning(f"Incorrect metric '{metric}'. Please check metric type.")
                metrics.remove(metric)
        return metrics

    @staticmethod
    def _format_attachments(attachments: str | list[str]) -> list[str]:
        return [attachment for attachment in set(attachments)] if isinstance(attachments, list) else [attachments]

    def _format_properties(
        self, properties: dict[str, str] | dict[str, int] | list[Property] | Property | None
    ) -> list[Property]:
        if properties is None:
            return []
        if isinstance(properties, Property):
            return [properties]
        if isinstance(properties, list):
            properties = self._remove_incorrect_properties(properties)
            key_list = [prop.key for prop in properties]
            self._check_key_duplicates(key_list)
            return properties
        if isinstance(properties, dict):
            return [Property(key, str(value)) for (key, value) in properties.items()]
        else:
            raise ValueError("Please check property type.")

    @staticmethod
    def _remove_incorrect_properties(properties: list[Property]) -> list[Property]:
        for prop in properties:
            if not isinstance(prop, Property):
                logging.warning(f"Incorrect property '{prop}'. Please check property type.")
                properties.remove(prop)
        return properties
