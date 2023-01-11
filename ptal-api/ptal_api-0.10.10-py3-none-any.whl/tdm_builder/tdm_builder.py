import logging
from abc import ABC, abstractmethod
from typing import Any, Union

from ..schema.api_schema import (
    Concept, ConceptLink, ConceptProperty, ConceptPropertyType
)


class AbstractTdmBuilder(ABC):
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

    @abstractmethod
    def reset_adding_restrictions(
        self, add_concepts: bool = True, add_links: bool = True,
        add_concept_properties: bool = True, add_link_properties: bool = True
    ):
        pass

    @abstractmethod
    def build_tdm(
        self, message: Union[str, dict], title: str, _uuid: str, url: str = None
    ):
        pass

    @abstractmethod
    def add_concept_fact(self, concept: Concept):
        pass

    @abstractmethod
    def add_link_fact(self, link: ConceptLink):
        pass

    @abstractmethod
    def add_concept_property_fact(
        self, concept_property: ConceptProperty, concept: Concept,
        value: Any, property_type: ConceptPropertyType
    ):
        pass

    @abstractmethod
    def add_link_property_fact(
        self, concept_property: ConceptProperty, link: ConceptLink,
        value: Any, link_property_type: ConceptPropertyType
    ):
        pass
