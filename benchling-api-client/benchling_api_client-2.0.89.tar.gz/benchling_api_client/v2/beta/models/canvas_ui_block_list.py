from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.button_ui_block import ButtonUiBlock
from ..models.chip_ui_block import ChipUiBlock
from ..models.dropdown_ui_block import DropdownUiBlock
from ..models.markdown_ui_block import MarkdownUiBlock
from ..models.search_input_ui_block import SearchInputUiBlock
from ..models.section_ui_block import SectionUiBlock
from ..models.selector_input_ui_block import SelectorInputUiBlock
from ..models.text_input_ui_block import TextInputUiBlock
from ..models.text_label_ui_block import TextLabelUiBlock
from ..types import UNSET, Unset

T = TypeVar("T", bound="CanvasUiBlockList")


@attr.s(auto_attribs=True, repr=False)
class CanvasUiBlockList:
    """  """

    _blocks: List[
        Union[
            ButtonUiBlock,
            ChipUiBlock,
            DropdownUiBlock,
            MarkdownUiBlock,
            SearchInputUiBlock,
            SectionUiBlock,
            SelectorInputUiBlock,
            TextInputUiBlock,
            TextLabelUiBlock,
            UnknownType,
        ]
    ]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("blocks={}".format(repr(self._blocks)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "CanvasUiBlockList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        blocks = []
        for blocks_item_data in self._blocks:
            if isinstance(blocks_item_data, UnknownType):
                blocks_item = blocks_item_data.value
            elif isinstance(blocks_item_data, ButtonUiBlock):
                blocks_item = blocks_item_data.to_dict()

            elif isinstance(blocks_item_data, ChipUiBlock):
                blocks_item = blocks_item_data.to_dict()

            elif isinstance(blocks_item_data, DropdownUiBlock):
                blocks_item = blocks_item_data.to_dict()

            elif isinstance(blocks_item_data, MarkdownUiBlock):
                blocks_item = blocks_item_data.to_dict()

            elif isinstance(blocks_item_data, SearchInputUiBlock):
                blocks_item = blocks_item_data.to_dict()

            elif isinstance(blocks_item_data, SectionUiBlock):
                blocks_item = blocks_item_data.to_dict()

            elif isinstance(blocks_item_data, SelectorInputUiBlock):
                blocks_item = blocks_item_data.to_dict()

            elif isinstance(blocks_item_data, TextInputUiBlock):
                blocks_item = blocks_item_data.to_dict()

            else:
                blocks_item = blocks_item_data.to_dict()

            blocks.append(blocks_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if blocks is not UNSET:
            field_dict["blocks"] = blocks

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_blocks() -> List[
            Union[
                ButtonUiBlock,
                ChipUiBlock,
                DropdownUiBlock,
                MarkdownUiBlock,
                SearchInputUiBlock,
                SectionUiBlock,
                SelectorInputUiBlock,
                TextInputUiBlock,
                TextLabelUiBlock,
                UnknownType,
            ]
        ]:
            blocks = []
            _blocks = d.pop("blocks")
            for blocks_item_data in _blocks:

                def _parse_blocks_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[
                    ButtonUiBlock,
                    ChipUiBlock,
                    DropdownUiBlock,
                    MarkdownUiBlock,
                    SearchInputUiBlock,
                    SectionUiBlock,
                    SelectorInputUiBlock,
                    TextInputUiBlock,
                    TextLabelUiBlock,
                    UnknownType,
                ]:
                    blocks_item: Union[
                        ButtonUiBlock,
                        ChipUiBlock,
                        DropdownUiBlock,
                        MarkdownUiBlock,
                        SearchInputUiBlock,
                        SectionUiBlock,
                        SelectorInputUiBlock,
                        TextInputUiBlock,
                        TextLabelUiBlock,
                        UnknownType,
                    ]
                    discriminator_value: str = cast(str, data.get("type"))
                    if discriminator_value is not None:
                        if discriminator_value == "BUTTON":
                            blocks_item = ButtonUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "CHIP":
                            blocks_item = ChipUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "DROPDOWN":
                            blocks_item = DropdownUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "LABEL":
                            blocks_item = TextLabelUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "MARKDOWN":
                            blocks_item = MarkdownUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SEARCH_INPUT":
                            blocks_item = SearchInputUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SECTION":
                            blocks_item = SectionUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SELECTOR_INPUT":
                            blocks_item = SelectorInputUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "TEXT_INPUT":
                            blocks_item = TextInputUiBlock.from_dict(data, strict=False)

                            return blocks_item

                        return UnknownType(value=data)
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = ButtonUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = ChipUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = DropdownUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = MarkdownUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SearchInputUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SectionUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SelectorInputUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = TextInputUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = TextLabelUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                blocks_item = _parse_blocks_item(blocks_item_data)

                blocks.append(blocks_item)

            return blocks

        try:
            blocks = get_blocks()
        except KeyError:
            if strict:
                raise
            blocks = cast(
                List[
                    Union[
                        ButtonUiBlock,
                        ChipUiBlock,
                        DropdownUiBlock,
                        MarkdownUiBlock,
                        SearchInputUiBlock,
                        SectionUiBlock,
                        SelectorInputUiBlock,
                        TextInputUiBlock,
                        TextLabelUiBlock,
                        UnknownType,
                    ]
                ],
                UNSET,
            )

        canvas_ui_block_list = cls(
            blocks=blocks,
        )

        canvas_ui_block_list.additional_properties = d
        return canvas_ui_block_list

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def blocks(
        self,
    ) -> List[
        Union[
            ButtonUiBlock,
            ChipUiBlock,
            DropdownUiBlock,
            MarkdownUiBlock,
            SearchInputUiBlock,
            SectionUiBlock,
            SelectorInputUiBlock,
            TextInputUiBlock,
            TextLabelUiBlock,
            UnknownType,
        ]
    ]:
        if isinstance(self._blocks, Unset):
            raise NotPresentError(self, "blocks")
        return self._blocks

    @blocks.setter
    def blocks(
        self,
        value: List[
            Union[
                ButtonUiBlock,
                ChipUiBlock,
                DropdownUiBlock,
                MarkdownUiBlock,
                SearchInputUiBlock,
                SectionUiBlock,
                SelectorInputUiBlock,
                TextInputUiBlock,
                TextLabelUiBlock,
                UnknownType,
            ]
        ],
    ) -> None:
        self._blocks = value
