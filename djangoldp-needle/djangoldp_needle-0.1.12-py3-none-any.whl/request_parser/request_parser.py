from .parsers import OpenGraph
from bs4 import BeautifulSoup
from ..models import AnnotationTarget


class RequestParser:
    def __init__(self):
        self.parsers = [
            OpenGraph()
        ]

    def parse(self, targe_url, target_html):
        beautiful_soup_document = BeautifulSoup(target_html, "html.parser")
        annotation_target = AnnotationTarget()
        parse_valid = False

        for parser in self.parsers:
            parser_parse_valid = parser.parse(annotation_target, targe_url, beautiful_soup_document,
                         parse_valid)
            parse_valid = parse_valid or parser_parse_valid

        return parse_valid, annotation_target
