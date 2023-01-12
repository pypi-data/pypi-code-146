from ai_dashboard.tabs.data_report.blocks.base import BaseBlock


class H1(BaseBlock):
    def __init__(self, content):
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {
                    "type": "heading",
                    "attrs": {"level": 1},
                    "content": self.preprocess_text_contents(content),
                }
            ],
        }


class H2(BaseBlock):
    def __init__(self, content):
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {
                    "type": "heading",
                    "attrs": {"level": 2},
                    "content": self.preprocess_text_contents(content),
                }
            ],
        }


class H3(BaseBlock):
    def __init__(self, content):
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {
                    "type": "heading",
                    "attrs": {"level": 3},
                    "content": self.preprocess_text_contents(content),
                }
            ],
        }


class Paragraph(BaseBlock):
    def __init__(self, content: str):
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {"type": "paragraph", "content": self.preprocess_text_contents(content)}
            ],
        }


class Code(BaseBlock):
    def __init__(self, text, language="python"):
        if not isinstance(text, str):
            raise TypeError("Code only accepts text type as input")
        # has to be text block.
        self.block = {
            "type": "codeBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "attrs": {"language": language},
            "content": [{"type": "text", "text": text}],
        }


P = Paragraph


class Space(BaseBlock):
    def __init__(self, height: int = 40):
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {"type": "spaceBlock", "attrs": {"width": "100%", "height": height}}
            ],
        }
