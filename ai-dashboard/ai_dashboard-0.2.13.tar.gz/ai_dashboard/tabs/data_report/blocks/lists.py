"""Blocks that can nest text blocks. They only accept content which is raw string, marks or a list of them."""
import numpy as np
from ai_dashboard.tabs.data_report.blocks.base import BaseBlock
from ai_dashboard.tabs.data_report.blocks.basic import Paragraph


class UnorderedList(BaseBlock):
    def _list_item(self, content, nested=False):
        # only takes a simple string and mark right now.
        return [
            {
                "type": "listItem",
                "content": [self._paragraph(content, exclude_appblock=True)],
            }
        ]

    def __init__(self, contents):
        if not isinstance(contents, list):
            raise TypeError("'contents' needs to be a List")
        output = []
        for c in contents:
            list_item = self._list_item(c)
            if not isinstance(list_item, list):
                list_item = [list_item]
            output += list_item
        self.block = {
            "type": "appBlock",
            "content": [{"type": "bulletList", "content": output}],
        }


class OrderedList(UnorderedList):
    def __init__(self, contents):
        if not isinstance(contents, list):
            raise TypeError("'contents' needs to be a List")
        output = []
        for c in contents:
            list_item = self._list_item(c)
            if not isinstance(list_item, list):
                list_item = [list_item]
            output += list_item
        self.block = {
            "type": "appBlock",
            "content": [{"type": "orderedList", "content": output}],
        }
