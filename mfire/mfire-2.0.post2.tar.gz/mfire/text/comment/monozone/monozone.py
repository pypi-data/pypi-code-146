from mfire.settings import get_logger

from mfire.text.comment.monozone import PeriodBuilder
from mfire.text.comment.representative_builder import RepresentativeValueManager
from mfire.utils.text_tools import (
    start_sentence_with_capital,
    transforme_syntaxe,
    modify_unit,
)
from mfire.composite.operators import ComparisonOperator


# Logging
LOGGER = get_logger(name="text_monozone.mod", bind="text_monozone")


class Monozone(PeriodBuilder, RepresentativeValueManager):
    """Builder spécifique pour gérer les composants de type "monozone"

    Args:
        Objet qui est capable de trouver et de et de fournir un modèle
        correspondant à self.reducer

    Inheritance:
        PeriodBuilder
        SynonymeBuilder
    """

    def compare_worst(
        self, first: float, second: float, operator: ComparisonOperator
    ) -> bool:
        """Permet de trouver la pire valeur en fonction de l'opérateur de comparaison

        Args:
            first (float): première valeur à comparer
            second (float): deuxième valeur à comparer
            operator (ComparisonOperator): opérateur de comparaison

        Returns:
            bool
        """

        if operator in (
            ComparisonOperator.SUP,
            ComparisonOperator.SUPEGAL,
        ):
            return first > second
        elif operator in (
            ComparisonOperator.INF,
            ComparisonOperator.INFEGAL,
        ):
            return first < second

    def compare_param(self, max_val: dict, key: str, param: dict) -> bool:
        """spécifique aux cumuls,
        on donne la valeur représentative du bloc de plus haute plain value
        si elles sont égales on prend celle du bloc de plus haute mountain value

        Args:
            max_val (dict): bloc de plus haute valeur représentative actuellement
            key (str): param étudié (ex EAU1__SOL)
            param (dict): infos du param

        Returns:
            bool: true si la valeur dans val max est la plus grande, false sinon
        """

        if self.compare_worst(
            max_val[key]["plain"]["value"],
            param["plain"]["value"],
            param["plain"]["operator"],
        ):
            return True
        elif param["plain"]["value"] == max_val[key]["plain"]["value"]:
            try:
                return self.compare_worst(
                    max_val[key]["mountain"]["value"],
                    param["mountain"]["value"],
                    param["mountain"]["operator"],
                )
            except AttributeError:
                return True
        else:
            return False

    def process_representative_value(self, reduction: dict) -> None:
        """Pour trouver la/les phrase(s) sur les valeurs représentatives
        - cas général on remplace la balise {Bi_val},
        - cas des cumuls on écrit à la fin de la phrase
            uniquement le bloc de plus haut niveau

        Args:
            reduction (dict): reduction en blocs
        """
        rep_value_table = dict()
        for bloc, data in reduction.items():
            if isinstance(data, dict):
                data_dict = {
                    k: v
                    for k, v in data.items()
                    if k not in ["start", "stop", "centroid_value"]
                }

                if not data_dict.get("level"):
                    data_dict["level"] = -1
                if bool(data_dict) and data_dict["level"] != 0:
                    rep_value_table[bloc + "_val"] = data_dict

        if reduction["type"] in ["SNOW", "PRECIP", "PRECIP_SNOW"]:
            # si on est un type cumul, on va donner la valeur représentative du niveau
            # max uniquement
            # on ajoute la phrase des cumuls en fin de phrase
            max_val = dict()
            for bloc, data in rep_value_table.items():
                if data["level"] == reduction["risk_max"]:
                    for key, param in data.items():
                        if key in max_val and self.compare_param(max_val, key, param):
                            pass
                        elif key != "level":
                            max_val[key] = param
            if bool(max_val):
                rep_value = self.process_value(max_val)[:-1]

            self.text += rep_value

        else:
            # si on est un type general on rempli au bon endroit
            # les valeurs représentatives dans le template
            final_rep_value = {
                key: self.process_value(
                    {k: v for k, v in value.items() if k != "level"}
                )[:-1]
                for key, value in rep_value_table.items()
                if len(value) > 1
            }

            self.text = self._text.format(**final_rep_value)

    def compute(self, reduction: dict) -> str:
        """génération du commentaire

        Args:
            reduction (dict): reduction par blocs
        """
        if reduction["template"] == "R.A.S.":
            return reduction["template"]

        self.build_period(reduction)
        self.process_representative_value(reduction)
        self.text = start_sentence_with_capital(self.text)
        self.text = transforme_syntaxe(self.text)
        self.text = modify_unit(self.text)

        name = reduction["compo_hazard"] + "_" + str(reduction["production_datetime"])
        # for_log = dict()
        # for_log[name] = dict()
        for_log = {
            name.replace(" ", "_"): {
                "level_max_demande": reduction["level_maxi"],
                "risk_max": reduction["risk_max"],
                "risk_min": reduction["risk_min"],
                "reduced": reduction["reduced"],
                "centroid": reduction["centroid"],
                "template": reduction["template"],
                "d_prod": str(reduction["production_datetime"]),
                "comment": self._text,
            }
        }

        # this log is used by tools/exploit_rejeu to generate various stats about
        # the monozone templates use. These tools explicitly parse the logs in search
        # for the string 'LOGINFO', so, as long we use them we need to keep it
        # (but only in debug since it is useless in production)
        LOGGER.debug(f"LOGINFO |{for_log}|")

        return self._text
