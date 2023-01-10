from bs4 import BeautifulSoup
import re


def _remove_html_tags(text):
    if text is None:
        return None

    no_html_text = BeautifulSoup(text, "html.parser").get_text()
    return no_html_text


class ObjectToText:
    def __init__(self, text, formats=None, show_preview=True):
        self.original_text = text
        self.show_preview = show_preview
        self.formats = formats or {
            "bold": {"start": "*", "end": "*"},
            "italic": {"start": "_", "end": "_"},
            "unispace": {"start": "```", "end": "```"},
            "none": {"start": "", "end": ""},
        }
        self.formatted_text = self.clean_text

    @property
    def clean_text(self):
        return _remove_html_tags(self.original_text)

    def _format(self, _format):
        return f"{self.formats[_format]['start']}{self.original_text}{self.formats[_format]['end']}"

    def to_bold(self):
        self.formatted_text = "\n \n" + self._format("bold") + "\n"
        return self

    def to_italic(self):
        self.formatted_text = self._format("italic")
        return self

    def to_unispace(self):
        self.formatted_text = self._format("unispace")
        return self

    def keep_spaces(self):
        self.formatted_text = self._format("none").replace(" ", "\u00A0")
        return self

    @property
    def to_json_structure(self):
        if not self.clean_text:
            self.formatted_text = None

        text_obj = {
            "type": "text/plain",
            "text": self.formatted_text + "\n" if self.formatted_text is not None else None
        }

        if not text_obj["text"]:
            return None

        return text_obj
