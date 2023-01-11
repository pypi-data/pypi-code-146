from __future__ import annotations

from dataclasses import dataclass

from semantha_sdk.model import SemanthaModelEntity, Paragraph


@dataclass(frozen=True)
class PageContent(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def paragraphs(self) -> list[Paragraph]:
        if "paragraphs" in self.data:
            return [
                Paragraph(raw_paragraph) for raw_paragraph in self.data["paragraphs"]
            ]
        else:
            return []

    # TODO tables DTO
    @property
    def tables(self):
        return None

    # TODO annotation page DTO
    @property
    def annotation_page(self):
        return None


class Page(SemanthaModelEntity):

    # def __init__(self, data: Union[dict, list]):
    #     super().__init__(data)

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def contents(self) -> list[PageContent]:
        return [PageContent(raw_content) for raw_content in self.data["contents"]]
