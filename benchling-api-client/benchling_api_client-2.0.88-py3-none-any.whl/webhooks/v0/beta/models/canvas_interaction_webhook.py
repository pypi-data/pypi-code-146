from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.canvas_interaction_webhook_type import CanvasInteractionWebhookType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CanvasInteractionWebhook")


@attr.s(auto_attribs=True, repr=False)
class CanvasInteractionWebhook:
    """ Sent when a user interacts with an app canvas via button press """

    _button_id: str
    _canvas_id: str
    _type: CanvasInteractionWebhookType
    _deprecated: bool
    _excluded_properties: List[str]

    def __repr__(self):
        fields = []
        fields.append("button_id={}".format(repr(self._button_id)))
        fields.append("canvas_id={}".format(repr(self._canvas_id)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("deprecated={}".format(repr(self._deprecated)))
        fields.append("excluded_properties={}".format(repr(self._excluded_properties)))
        return "CanvasInteractionWebhook({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        button_id = self._button_id
        canvas_id = self._canvas_id
        type = self._type.value

        deprecated = self._deprecated
        excluded_properties = self._excluded_properties

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if button_id is not UNSET:
            field_dict["buttonId"] = button_id
        if canvas_id is not UNSET:
            field_dict["canvasId"] = canvas_id
        if type is not UNSET:
            field_dict["type"] = type
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated
        if excluded_properties is not UNSET:
            field_dict["excludedProperties"] = excluded_properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_button_id() -> str:
            button_id = d.pop("buttonId")
            return button_id

        try:
            button_id = get_button_id()
        except KeyError:
            if strict:
                raise
            button_id = cast(str, UNSET)

        def get_canvas_id() -> str:
            canvas_id = d.pop("canvasId")
            return canvas_id

        try:
            canvas_id = get_canvas_id()
        except KeyError:
            if strict:
                raise
            canvas_id = cast(str, UNSET)

        def get_type() -> CanvasInteractionWebhookType:
            _type = d.pop("type")
            try:
                type = CanvasInteractionWebhookType(_type)
            except ValueError:
                type = CanvasInteractionWebhookType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(CanvasInteractionWebhookType, UNSET)

        def get_deprecated() -> bool:
            deprecated = d.pop("deprecated")
            return deprecated

        try:
            deprecated = get_deprecated()
        except KeyError:
            if strict:
                raise
            deprecated = cast(bool, UNSET)

        def get_excluded_properties() -> List[str]:
            excluded_properties = cast(List[str], d.pop("excludedProperties"))

            return excluded_properties

        try:
            excluded_properties = get_excluded_properties()
        except KeyError:
            if strict:
                raise
            excluded_properties = cast(List[str], UNSET)

        canvas_interaction_webhook = cls(
            button_id=button_id,
            canvas_id=canvas_id,
            type=type,
            deprecated=deprecated,
            excluded_properties=excluded_properties,
        )

        return canvas_interaction_webhook

    @property
    def button_id(self) -> str:
        if isinstance(self._button_id, Unset):
            raise NotPresentError(self, "button_id")
        return self._button_id

    @button_id.setter
    def button_id(self, value: str) -> None:
        self._button_id = value

    @property
    def canvas_id(self) -> str:
        if isinstance(self._canvas_id, Unset):
            raise NotPresentError(self, "canvas_id")
        return self._canvas_id

    @canvas_id.setter
    def canvas_id(self, value: str) -> None:
        self._canvas_id = value

    @property
    def type(self) -> CanvasInteractionWebhookType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: CanvasInteractionWebhookType) -> None:
        self._type = value

    @property
    def deprecated(self) -> bool:
        if isinstance(self._deprecated, Unset):
            raise NotPresentError(self, "deprecated")
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value: bool) -> None:
        self._deprecated = value

    @property
    def excluded_properties(self) -> List[str]:
        """These properties have been dropped from the payload due to size."""
        if isinstance(self._excluded_properties, Unset):
            raise NotPresentError(self, "excluded_properties")
        return self._excluded_properties

    @excluded_properties.setter
    def excluded_properties(self, value: List[str]) -> None:
        self._excluded_properties = value
