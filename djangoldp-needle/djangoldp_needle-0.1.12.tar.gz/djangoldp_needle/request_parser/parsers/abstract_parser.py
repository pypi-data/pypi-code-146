from abc import ABC, abstractmethod


class AbstractParser(ABC):
    @abstractmethod
    def parse(self, annotation_target, target_url, bs_document, previous_parse_result):
        pass