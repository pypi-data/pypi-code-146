from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.experiment_parameters import ExperimentParameters
    from ..models.report import Report


T = TypeVar("T", bound="Experiment")


@attr.s(auto_attribs=True)
class Experiment:
    """
    Attributes:
        duration (int):
        engine (str):
        label (str):
        models (int):
        name (str):
        parameters (ExperimentParameters):
        quality (int):
        running (bool):
        timestamp (int):
        uptodate (bool):
        classes (Union[Unset, List[str]]):
        email_notification (Union[Unset, bool]):
        favorite (Union[Unset, bool]):
        report (Union[Unset, Report]):
        tags (Union[Unset, List[str]]):
    """

    duration: int
    engine: str
    label: str
    models: int
    name: str
    parameters: "ExperimentParameters"
    quality: int
    running: bool
    timestamp: int
    uptodate: bool
    classes: Union[Unset, List[str]] = UNSET
    email_notification: Union[Unset, bool] = UNSET
    favorite: Union[Unset, bool] = UNSET
    report: Union[Unset, "Report"] = UNSET
    tags: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        duration = self.duration
        engine = self.engine
        label = self.label
        models = self.models
        name = self.name
        parameters = self.parameters.to_dict()

        quality = self.quality
        running = self.running
        timestamp = self.timestamp
        uptodate = self.uptodate
        classes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.classes, Unset):
            classes = self.classes

        email_notification = self.email_notification
        favorite = self.favorite
        report: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.report, Unset):
            report = self.report.to_dict()

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "duration": duration,
                "engine": engine,
                "label": label,
                "models": models,
                "name": name,
                "parameters": parameters,
                "quality": quality,
                "running": running,
                "timestamp": timestamp,
                "uptodate": uptodate,
            }
        )
        if classes is not UNSET:
            field_dict["classes"] = classes
        if email_notification is not UNSET:
            field_dict["emailNotification"] = email_notification
        if favorite is not UNSET:
            field_dict["favorite"] = favorite
        if report is not UNSET:
            field_dict["report"] = report
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.experiment_parameters import ExperimentParameters
        from ..models.report import Report

        d = src_dict.copy()
        duration = d.pop("duration")

        engine = d.pop("engine")

        label = d.pop("label")

        models = d.pop("models")

        name = d.pop("name")

        parameters = ExperimentParameters.from_dict(d.pop("parameters"))

        quality = d.pop("quality")

        running = d.pop("running")

        timestamp = d.pop("timestamp")

        uptodate = d.pop("uptodate")

        classes = cast(List[str], d.pop("classes", UNSET))

        email_notification = d.pop("emailNotification", UNSET)

        favorite = d.pop("favorite", UNSET)

        _report = d.pop("report", UNSET)
        report: Union[Unset, Report]
        if isinstance(_report, Unset):
            report = UNSET
        else:
            report = Report.from_dict(_report)

        tags = cast(List[str], d.pop("tags", UNSET))

        experiment = cls(
            duration=duration,
            engine=engine,
            label=label,
            models=models,
            name=name,
            parameters=parameters,
            quality=quality,
            running=running,
            timestamp=timestamp,
            uptodate=uptodate,
            classes=classes,
            email_notification=email_notification,
            favorite=favorite,
            report=report,
            tags=tags,
        )

        return experiment
