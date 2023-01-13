from mfire.settings import get_logger
from mfire.text.period_describer import PeriodDescriber
from mfire.text.base import BaseBuilder
from mfire.utils.date import Period


# Logging
LOGGER = get_logger(name="text_builder.mod", bind="text_builder")


class PeriodBuilder(BaseBuilder):
    """Permet  de traiter  les balises de période dans un commentaire.

    Inheritance:
        Builder
    """

    def build_period(self, reduction: dict) -> None:
        """Remplie le template avec des éléments de périodes
        Balises ciblées du type {Bi_period} {Bi_start} {Bi_stop}

        Args:
            reduction (dict): dictionnaire contenant les informations
        """
        prod_date = reduction["production_datetime"]
        period_table = dict()
        for k, v in reduction.items():
            if isinstance(v, dict) and "start" in v and "stop" in v:
                period = PeriodDescriber(prod_date).describe(
                    Period(v["start"], v["stop"])
                )
                start = PeriodDescriber(prod_date).describe(Period(v["start"]))
                stop = PeriodDescriber(prod_date).describe(Period(v["stop"]))
                period_table[k + "_period"] = period
                period_table[k + "_start"] = start
                period_table[k + "_stop"] = stop

        self.text = self._text.format(**period_table)
