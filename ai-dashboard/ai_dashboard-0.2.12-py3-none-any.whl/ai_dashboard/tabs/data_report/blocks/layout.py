"""Layout blocks can nest almost any other blocks"""
from ai_dashboard.tabs.data_report.blocks.base import BaseBlock
from ai_dashboard.tabs.data_report.blocks.basic import Paragraph

##Below is still WIP
class ColumnsBlock(BaseBlock):
    def _column_block(self, block, report_client=None):
        return {"type": "columnContent", "content": [self.preprocess_block(block)]}

    def __init__(self, list_of_blocks, num_columns: int = 2):
        if not isinstance(list_of_blocks, list):
            raise TypeError("'blocks' needs to be a List")
        self.num_columns = num_columns
        self.blocks = list_of_blocks
        input_blocks = []
        for c in self.blocks:
            input_blocks += self._column_block(c)
        self.block = {
            "type": "appBlock",
            "content": [
                {
                    "type": "columnBlock",
                    "attrs": {"columns": self.num_columns},
                    "content": input_blocks,
                }
            ],
        }

    def postprocess(self, report_client=None):
        input_blocks = []
        for block in self.blocks:
            if issubclass(type(block), BaseBlock):
                input_blocks.append(
                    self._column_block(block(report_client=report_client))
                )
            else:
                input_blocks.append(self._column_block(block))
        self.block = {
            "type": "appBlock",
            "content": [
                {
                    "type": "columnBlock",
                    "attrs": {"columns": self.num_columns},
                    "content": input_blocks,
                }
            ],
        }


class CardBlock(BaseBlock):
    def __init__(self, contents, width, color):
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {
                    "type": "cardBlock",
                    "attrs": {"width": width, "colour": color},
                    "content": contents,
                }
            ],
        }


class Tooltip(BaseBlock):
    def __init__(self, content, tooltip_text):
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {
                    "type": "tooltip",
                    "attrs": {"content": tooltip_text},
                    "content": self.preprocess_text_contents(content),
                }
            ],
        }


class DetailsBlock(BaseBlock):
    def __init__(self, title_content, contents, collapsed: bool = True):
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {
                    "type": "details",
                    "attrs": {"open": collapsed},
                    "content": [
                        {
                            "type": "detailsSummary",
                            "content": [self.preprocess_block(title_content)],
                        },
                        {
                            "type": "detailsContent",
                            "content": [self.preprocess_block(c) for c in contents],
                        },
                    ],
                }
            ],
        }


class QuoteBlock(BaseBlock):
    def __init__(self, content):
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {"type": "blockquote", "content": self.preprocess_content(content)}
            ],
        }
