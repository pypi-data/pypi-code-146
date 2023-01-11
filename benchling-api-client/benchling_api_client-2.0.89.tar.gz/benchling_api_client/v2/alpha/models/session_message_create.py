from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.session_message_style import SessionMessageStyle
from ..types import UNSET, Unset

T = TypeVar("T", bound="SessionMessageCreate")


@attr.s(auto_attribs=True, repr=False)
class SessionMessageCreate:
    """  """

    _content: str
    _style: Union[Unset, SessionMessageStyle] = SessionMessageStyle.NONE

    def __repr__(self):
        fields = []
        fields.append("content={}".format(repr(self._content)))
        fields.append("style={}".format(repr(self._style)))
        return "SessionMessageCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        content = self._content
        style: Union[Unset, int] = UNSET
        if not isinstance(self._style, Unset):
            style = self._style.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if content is not UNSET:
            field_dict["content"] = content
        if style is not UNSET:
            field_dict["style"] = style

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_content() -> str:
            content = d.pop("content")
            return content

        try:
            content = get_content()
        except KeyError:
            if strict:
                raise
            content = cast(str, UNSET)

        def get_style() -> Union[Unset, SessionMessageStyle]:
            style = UNSET
            _style = d.pop("style")
            if _style is not None and _style is not UNSET:
                try:
                    style = SessionMessageStyle(_style)
                except ValueError:
                    style = SessionMessageStyle.of_unknown(_style)

            return style

        try:
            style = get_style()
        except KeyError:
            if strict:
                raise
            style = cast(Union[Unset, SessionMessageStyle], UNSET)

        session_message_create = cls(
            content=content,
            style=style,
        )

        return session_message_create

    @property
    def content(self) -> str:
        """ A message string, to be rendered as plain text with Benchling chips. References to Benchling items (up to 10 per msg) will be rendered as chips in the Benchling UX. A valid reference is a Benchling API id, prefixed with "id:" and contained by braces. For example: "{id:ent_a0SApq3}." """
        if isinstance(self._content, Unset):
            raise NotPresentError(self, "content")
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        self._content = value

    @property
    def style(self) -> SessionMessageStyle:
        if isinstance(self._style, Unset):
            raise NotPresentError(self, "style")
        return self._style

    @style.setter
    def style(self, value: SessionMessageStyle) -> None:
        self._style = value

    @style.deleter
    def style(self) -> None:
        self._style = UNSET
