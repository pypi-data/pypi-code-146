"""Layout blocks can nest almost any other blocks"""
from ai_dashboard.tabs.data_report.blocks.base import BaseBlock


class ColumnContent(BaseBlock):
    def __init__(self, blocks):
        self.input_blocks = blocks
        self.block = {"type": "columnContent", "content": self.input_blocks}

    def postprocess(self, report_client=None):
        self.block = {
            "type": "columnContent",
            "content": self.postprocess_blocks(
                self.input_blocks, report_client=report_client
            ),
        }


class Columns(BaseBlock):
    def __init__(self, column_items, num_columns: int = 0):
        if not isinstance(column_items, list):
            raise TypeError("'column_items' needs to be a list")
        for c in column_items:
            if isinstance(c, dict):
                if "type" not in c or c["type"] != "columnContent":
                    raise TypeError(
                        "column in 'column_items' needs to be a ColumnContent"
                    )
            elif not isinstance(c, ColumnContent):
                print(type(c))
                raise TypeError("column in 'column_items' needs to be a ColumnContent")

        if num_columns:
            self.num_columns = num_columns
        else:
            self.num_columns = len(column_items)
        self.column_items = column_items
        self.block = {
            "type": "appBlock",
            "content": [
                {
                    "type": "columnBlock",
                    "attrs": {"columns": self.num_columns},
                    "content": self.column_items,
                }
            ],
        }

    def postprocess(self, report_client=None):
        self.block = {
            "type": "appBlock",
            "content": [
                {
                    "type": "columnBlock",
                    "attrs": {"columns": self.num_columns},
                    "content": self.postprocess_blocks(self.column_items),
                }
            ],
        }


class Card(BaseBlock):
    def __init__(self, blocks, width, color):
        self.input_blocks = blocks
        self.width = width
        self.color = color
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {
                    "type": "cardBlock",
                    "attrs": {"width": width, "colour": color},
                    "content": blocks,
                }
            ],
        }

    def postprocess(self, report_client=None):
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {
                    "type": "cardBlock",
                    "attrs": {"width": self.width, "colour": self.color},
                    "content": self.postprocess_blocks(
                        self.input_blocks, report_client=report_client
                    ),
                }
            ],
        }


class Tooltip(BaseBlock):
    def __init__(self, blocks, tooltip_text):
        self.tooltip_text = tooltip_text
        self.input_blocks = blocks
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {
                    "type": "tooltip",
                    "attrs": {"content": tooltip_text},
                    "content": self.input_blocks,
                }
            ],
        }

    def postprocess(self, report_client=None):
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {
                    "type": "tooltip",
                    "attrs": {"content": self.tooltip_text},
                    "content": self.postprocess_blocks(
                        self.input_blocks, report_client=report_client
                    ),
                }
            ],
        }


class Quote(BaseBlock):
    def __init__(self, blocks):
        self.input_blocks = blocks
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [{"type": "blockquote", "content": blocks}],
        }

    def postprocess(self, report_client=None):
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {
                    "type": "blockquote",
                    "content": self.postprocess_blocks(
                        self.input_blocks, report_client=report_client
                    ),
                }
            ],
        }


class Details(BaseBlock):
    # This doesnt work in the frontend?
    def __init__(self, blocks, title_content, collapsed: bool = True):
        self.collapsed = collapsed
        self.input_blocks = blocks
        self.title_content = title_content
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {
                    "type": "details",
                    "attrs": {"open": self.collapsed},
                    "content": [
                        {
                            "type": "detailsSummary",
                            "content": self.preprocess_text_contents(title_content),
                        },
                        {
                            "type": "detailsContent",
                            "content": self.input_blocks,
                        },
                    ],
                }
            ],
        }

    def postprocess(self, report_client=None):
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {
                    "type": "details",
                    "attrs": {"open": self.collapsed},
                    "content": [
                        {
                            "type": "detailsSummary",
                            "content": self.preprocess_text_contents(
                                self.title_content
                            ),
                        },
                        {
                            "type": "detailsContent",
                            "content": self.postprocess_blocks(
                                self.input_blocks, report_client=report_client
                            ),
                        },
                    ],
                }
            ],
        }
