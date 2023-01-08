# FlexiRPG -- HTML to plain text converter.
#
# Copyright 2020 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from html.parser import HTMLParser


class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []

    def handle_data(self, d):
        self.result.append(d)

    def get_text(self):
        return "".join(self.result)


def html_to_text(html: str):
    """Convert 'html' to plain text by removing all HTML tags."""
    s = HTMLTextExtractor()
    s.feed(html)
    return s.get_text()
