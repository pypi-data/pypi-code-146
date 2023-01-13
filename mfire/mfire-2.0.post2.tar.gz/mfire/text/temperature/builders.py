import re

from mfire.settings import get_logger
from mfire.text.base import BaseBuilder
from mfire.text.common import (
    SynonymeBuilder,
    ZoneBuilder,
    PeriodBuilder,
    TemplateBuilder,
)

from mfire.text.template import read_file
from mfire.settings import TEMPLATES_FILENAMES, LANGUAGE
from mfire.text.temperature import TemperatureSelector


# Logging
LOGGER = get_logger(name="temperature_builder.mod", bind="temperature_builder")

TEMPE_TPL_RETRIEVER = read_file(TEMPLATES_FILENAMES["fr"]["synthesis"]["temperature"])


class TemperatureBuilder(
    TemplateBuilder,
    SynonymeBuilder,
    PeriodBuilder,
    ZoneBuilder,
    BaseBuilder,
):
    """Builder spécifique pour gérer les textes de sythèse pour la température

    Args:
        Objet qui est capable de trouver et de et de fournir un modèle
        correspondant à self.reducer.

    Inheritance:
        BaseBuilder
        SynonymeBuilder
        ZoneBuilder
        PeriodBuilder
    """

    # pattern used to fix inervals with only one value
    pattern = re.compile(rf"(\d+) {LANGUAGE.a_grave} (\d+)")

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    def fix_single_value_intervals(self) -> str:
        """removes duplicate temperature for intervals with a single value
        e.g: "de 12 à 12° dans le Vercors" => "12° dans le Vercors"

        Args:
            text (str): the description text to be fixed

        Returns:
            str: the fixed description text
        """

        for match in TemperatureBuilder.pattern.finditer(self._text):
            interval_text = match.group(0)
            t1 = match.group(1)
            t2 = match.group(2)
            if t1 == t2:
                self._text = self._text.replace(interval_text, t2)

        return self._text

    def prettify_altitude_intervals(self):
        pass

    def to_upper(self):
        """Set the first letter of the sentence to upper case"""
        self._text = self._text[0].upper() + self._text[1:]

    def post_process(self) -> str:
        """Cleans up the generated text to make it more humanlike"""

        self.fix_single_value_intervals()
        self.prettify_altitude_intervals()
        self.to_upper()

    def compute(self, reduction: dict) -> None:
        self.reset()
        self.reduction = reduction
        selector = TemperatureSelector()
        key = self.find_template_key(selector)
        self.retrieve_template(key, TEMPE_TPL_RETRIEVER)
        self.handle_comment(reduction)
        self.build_period(reduction)
        self.build_zone()
        self.find_synonyme()
        self.post_process()
        LOGGER.info(self._text)
