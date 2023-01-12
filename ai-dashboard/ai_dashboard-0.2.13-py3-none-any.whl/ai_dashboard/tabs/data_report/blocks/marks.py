"""Marks for accenting basic text blocks"""
from ai_dashboard.tabs.data_report.blocks import BaseMark


class BoldMark(BaseMark):
    def __init__(self, content):
        self.mark = [{"type": "bold"}]
        self.block = self.preprocess_mark(content, self.mark)


class ItalicMark(BaseMark):
    def __init__(self, content):
        self.mark = [{"type": "italic"}]
        self.block = self.preprocess_mark(content, self.mark)


class StrikeMark(BaseMark):
    def __init__(self, content):
        self.mark = [{"type": "strike"}]
        self.block = self.preprocess_mark(content, self.mark)


class UnderlineMark(BaseMark):
    def __init__(self, content):
        self.mark = [{"type": "underline"}]
        self.block = self.preprocess_mark(content, self.mark)


class InlineCodeMark(BaseMark):
    def __init__(self, content):
        self.mark = [{"type": "code"}]
        self.block = self.preprocess_mark(content, self.mark)


class HighlightMark(BaseMark):
    def __init__(self, content, start, end, color):
        self.mark = [
            {
                "type": "highlight",
                "attrs": {"color": color},
                "from": start,
                "to": end,
            }
        ]
        self.block = self.preprocess_mark(content, self.mark)


class ColorMark(BaseMark):
    def __init__(self, content, color, background_color):
        self.mark = [
            {
                "type": "textStyle",
                "attrs": {"color": color, "backgroundColor": background_color},
            }
        ]
        self.block = self.preprocess_mark(content, self.mark)


class LinkMark(BaseMark):
    def __init__(self, content, href):
        self.mark = [{"type": "link", "attrs": {"href": href, "target": "_blank"}}]
        self.block = self.preprocess_mark(content, self.mark)
