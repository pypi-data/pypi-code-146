"""
@package text.comment.__init__

Module for representative value in detailed comment
"""

# Standard packages
import re
from typing import Optional, Tuple
import numpy as np

# Own package
from mfire.settings import Settings, TEMPLATES_FILENAMES
from mfire.settings import get_logger
from mfire.utils.formatter import get_synonym
from mfire.composite.operators import ComparisonOperator
from mfire.text.template import Template, read_file
from mfire.text.comment.multizone import ComponentInterface
from mfire.text.base import BaseBuilder
from mfire.configuration.rules import CommonRules


# Logging
LOGGER = get_logger(
    name="text.representative_builder.mod", bind="text.representative_builder"
)


def split_var_name(var_name: str) -> Tuple[str, Optional[int], Optional[str]]:
    """Splits a variable name following the pattern <prefix><accum>__<vertical_level>
    into a tuple (<prefix>, <accum>, <vertical_level>).

    Args:
        var_name (str): Variable name

    Returns:
        Tuple[str, Optional[int], Optional[str]]: Tuple containing the:
            - prefix
            - the accumulation value (optional)
            - the vertical level (optional)
    """
    prefix, accum, vert_level = re.match(
        r"^([a-zA-Z_]+)(\d*)__(.*)$", var_name
    ).groups()
    if accum == "":
        accum = 0
    accum = int(accum)
    return prefix, accum, vert_level


class RepresentativeValueManager(BaseBuilder):
    """
    This class enable to manage all text for representative values.
    It chooses which class needs to be used for each case.
    """

    # used to retrieve the base param name from its aggregated form
    rules = CommonRules()
    aggregation_rules = rules.agg_param_df
    family_rules = rules.family_param_df

    def process_value(self, reduction: dict = None) -> str | None:
        """
        On process les différentes valeurs représentatives.
        S'il n'y en a pas, théoriquement on ne fait rien.
        Chaque valeur représentative est processée.
        si une reduction est passée c'est qu'on est dans le cas monozone
        """
        if reduction:
            dict_value = reduction
            module = "monozone"
        else:
            # Your IDE is probably panicking beacuse it doesnt find where
            # self.component_handler comes froms
            # It is declared, not in this class, nor in its parent but in
            # mfire.text.comment.multizone.Multizone(), which is a child of this
            # class. Sometimes I miss my compiler...
            dict_value = self.component_handler.get_critical_value()
            module = "multizone"

        altitudes = [
            v["mountain_altitude"]
            for v in dict_value.values()
            if "mountain_altitude" in v
        ]

        if (len(altitudes) == len(dict_value)) and (len(set(altitudes)) == 1):
            # dans le cas d'un composant de type Bertrand on va changer gérer
            # toutes les variables de neige cumulées ensemble.
            self.text += AltitudeBuilder().add_variable_value(
                variable="_", dict_in=dict_value
            )
            return None

        # Sinon pour l'instant on ajoute une phrase pour chacune des variables présente.
        val_rep = ""
        # Chaque phrase est construite de la même manière.

        # we don't build a phrase when in a case of a complex risk
        # (composition of atomic risks) except if the risks are of the same type
        # e.g.: if a risk is triggerd by either wind or snow => no description
        # but if a risk is either snow__1H or snow_24H => we build a description
        # if a risk is FF and FF_RAF => we also build a description
        are_values_homogenous = self.are_values_homogenous(dict_value)
        if len(dict_value) == 1 or are_values_homogenous:
            for key in dict_value:
                prefix, _, _ = split_var_name(key)
                if prefix == "FF":
                    value_builder = FFBuilder()
                elif prefix == "RAF":
                    value_builder = FFRafBuilder()
                elif prefix == "T":
                    value_builder = TemperatureBuilder()
                elif prefix in ["PRECIP", "EAU"]:
                    value_builder = PrecipBuilder()
                elif prefix == "NEIPOT":
                    value_builder = SnowBuilder()
                else:
                    LOGGER.warning(
                        "We don't know how to speak about this parameter.",
                        prefix=prefix,
                        var_name=key,
                    )
                    value_builder = None
                if module == "monozone":
                    if value_builder is None:
                        return ""
                    val_rep += value_builder.add_variable_value(key, dict_value[key])
                else:
                    if value_builder is not None:
                        self.text += value_builder.add_variable_value(
                            key, dict_value[key]
                        )
        return val_rep

    def are_values_homogenous(self, dict_params) -> bool:
        """checks uf all the parameters represent the same phenomemnon,
        but with different time aggregations.
        e.g:
        ['NEIPOT__1H', 'NEIPOT__6H', 'NEIPOT__24H'] returns True
        ['NEIPOT_1H', 'FF_RAF__1H'] returns False
        ['FF', 'FF_RAF'] returns

        Args:
            dict_params (_type_): all the parameters that are trigered an alert

        Returns:
            bool: True if all the parameters are similar, False otherwise
        """
        family = None
        for param, _ in dict_params.items():

            param_family = None

            # we search for the base name of the current param
            if param in self.aggregation_rules.index:
                base_param = self.aggregation_rules.loc[param]["param"]
            else:
                base_param, _, _ = split_var_name(param)

            # then we look for its family
            if base_param in self.family_rules.index:
                param_family = self.family_rules.loc[base_param]["family"]
            else:
                LOGGER.info(f"Could not find a family for {param}.")
                return False

            if family is None:
                family = param_family

            # this param is different from the reference, no need to serach further
            if param_family != family:
                return False

        return True

    def process(self, component_handler: ComponentInterface) -> None:
        """process: creates and processes a new detailed comment, accessible
        through the self.text property

        Args:
            component_handler (ComponentInterface): Component for which
                the detailed comment is being processed.
        """
        super().process(component_handler)
        self.process_value()


class RepresentativeValueBuilder(BaseBuilder):
    """
    This class enable to speak about representative values
    """

    cumul_var = ["NEIPOT", "PRECIP", "EAU"]

    pheno = ""
    def_article = ""
    indef_article = ""
    feminin = False

    template_retriever = read_file(
        TEMPLATES_FILENAMES[Settings().language]["multizone"]["rep_val"]
    )
    seed = None  # Permettra de fixer la seed pour des tests

    environ_list = ["aux alentours de"]

    def get_accum(self, variable):
        """
        Permet d'avoir le nombre d'heure sur lequel la variable est cumulé.

        Args:
            variable (str): Le nom de la variable

        Returns:
            [str]: le nombre d'heure sur lequel la variable est cumulée
        """
        _, accum, _ = split_var_name(variable)

        if not accum:
            return ""

        accum_text = f"{accum} heure"
        if int(accum) > 1:
            accum_text += "s"

        return accum_text

    def get_variable_intro(self, variable):
        """
        Récupère la manière de parler de la variable
        """
        return f"{self.def_article} {self.pheno}"

    def get_variable_d(self, variable):
        """
        Permet d'avoir la variable (commençant par d)

        Args:
            variable (str): La variable (pas utilisé ici mais dans des classes filles)

        Returns:
            (str): Le choix pour la variable
        """
        return f"{self.indef_article} {self.pheno}"

    def environ(self):
        """
        Choisi comment dire environ
        """
        return get_synonym(self.environ_list[0]) + " "

    @staticmethod
    def units(unit):
        """
        On récupère l'unité. Si elle est à None on met un blanc.
        """
        if unit is None:
            return ""
        return unit

    def get_format(self, variable):
        """
        On récupère les informations qui sont potentiellement utilisé dans les phrases.
        """
        return {
            "pheno": self.pheno,
            "var": self.get_variable_intro(variable),
            "var_d": self.get_variable_d(variable),
            "feminin": "e" if self.feminin else "",
            "environ": self.environ(),
        }

    def get_sentence(self, variable, sentence_type):
        """
        Choix de la phrase de base.
        """
        default = (
            f"Echec dans la récupération du template"
            f"(key={sentence_type}, var={variable}) (error COM-001)."
        )
        sentence = self.template_retriever.get(key=sentence_type, default=default)
        return Template(sentence)

    def rounding(self, x: float, **kwargs) -> str:
        """
        Fonction spécifique à implémenter pour chaque variable.
        """
        if x is not None and abs(x) >= 1e-6:
            return str(x)
        return None

    @staticmethod
    def modify_environ(format_table, rep_value, sentence):
        if str(rep_value).startswith("au"):
            format_table["environ"] = "d'"
            sentence = sentence.replace("{environ} ", " {environ}")
        elif str(rep_value).startswith("de"):
            format_table["environ"] = ""
        return sentence

    @staticmethod
    def replace_critical(dict_in):
        if dict_in.get("next_critical", None) is not None and ComparisonOperator(
            dict_in["operator"]
        )(dict_in["value"], dict_in["next_critical"]):
            rep_value = (
                dict_in["next_critical"]
                + (dict_in["next_critical"] - dict_in["value"]) / 100
            )
            local = dict_in["value"]
            LOGGER.debug(
                f"On remplace la valeur critique {local} {rep_value} {dict_in}"
            )
        else:
            rep_value = dict_in["value"]
            local = None
        return (rep_value, local)

    def identify_case(self, variable: str, dict_in: dict):
        """
        Cette fonction identifie le cas a traiter.
        Elle commence à remplir le tableau.

        Args:
            variable (str): La variable d'intérêt
            dict_in (dict): Le dictionnaire
        """
        speak = None
        local_plain = None
        local_mountain = None
        rep_plain = None
        format_table = self.get_format(variable)
        if "plain" in dict_in:
            operator = dict_in["plain"].get("operator")
            rep_value, local = self.replace_critical(dict_in["plain"])
            rep_plain = self.rounding(
                rep_value,
                operator=operator,
                environ=format_table["environ"],
            )
            if local is not None:
                local_plain = self.rounding(
                    local,
                    operator=operator,
                    environ=format_table["environ"],
                )
                if local_plain == rep_plain:
                    local_plain = None
                else:
                    format_table["local_value"] = " ".join(
                        [str(local_plain), self.units(dict_in["plain"]["units"])]
                    )
            else:
                local_plain = None
            format_table["value"] = " ".join(
                [str(rep_plain), self.units(dict_in["plain"]["units"])]
            )

            speak = "plain"

        if "mountain" in dict_in:
            rep_value, local = self.replace_critical(dict_in["mountain"])
            operator = dict_in["mountain"].get("operator")
            # On regarde si la condition est remplie sur la montagne
            rep_mountain = self.rounding(
                rep_value,
                operator=operator,
                environ=format_table["environ"],
            )
            format_table["mountain_value"] = " ".join(
                [str(rep_mountain), self.units(dict_in["mountain"]["units"])]
            )
            format_table["hauteur"] = "sur les hauteurs"
            format_table["altitude"] = dict_in.get("mountain_altitude")

            if local is not None:
                local_mountain = self.rounding(
                    local,
                    operator=operator,
                    environ=format_table["environ"],
                )
                if local_mountain == rep_mountain:
                    local_mountain = None
                else:
                    format_table["local_mountain_value"] = " ".join(
                        [str(local_mountain), self.units(dict_in["mountain"]["units"])]
                    )
            else:
                local_mountain = None

            if rep_plain is not None:
                # On reprend ce qui etait dans le module de Lamyaa
                if rep_plain != rep_mountain or (
                    local_mountain is not None and local_mountain != local_plain
                ):
                    speak = "plain_mountain"
                else:
                    speak = "plain"
            else:
                speak = "mountain"

        return (speak, format_table, local_plain, local_mountain)

    def add_variable_value(self, variable: str, dict_in: dict):
        """
        Pour la variable en question, on va voir si on parle que de la valeur sur
        la plaine ou  de la valeur sur la plaine et de la valeur en montagne.
        Pour l'instant la phrase est la même qu'il y ai une ou plusieurs variables.
        """
        speak, format_table, local_plain, local_mountain = self.identify_case(
            variable, dict_in
        )
        # On va maitnenant faire un arbre de décision pour savoir le type de
        # phrase à charger.

        if speak == "plain" and local_plain is None:
            sentence_type = "plain"
        elif speak == "plain" and local_plain is not None:
            sentence_type = "local_plain"
        elif speak == "mountain" and local_mountain is None:
            sentence_type = "mountain"
        elif speak == "mountain" and local_mountain is not None:
            sentence_type = "local_mountain"
        elif (
            speak == "plain_mountain" and local_plain is None and local_mountain is None
        ):
            sentence_type = "plain_mountain"
        elif (
            speak == "plain_mountain"
            and local_plain is not None
            and local_mountain is None
        ):
            sentence_type = "local_plain_mountain"
        elif (
            speak == "plain_mountain"
            and local_plain is None
            and local_mountain is not None
        ):
            sentence_type = "plain_local_mountain"
        elif (
            speak == "plain_mountain"
            and local_plain is not None
            and local_mountain is not None
        ):
            sentence_type = "local_plain_local_mountain"

        sentence = self.get_sentence(variable, sentence_type)
        sentence = self.modify_environ(format_table, format_table["value"], sentence)
        return sentence.format(**format_table)

    def add_short_description(
        self, var_name: str, dict_in: dict, case: str = "short"
    ) -> str:
        format_table = self.get_format(var_name)

        # calcul de la valeur representative et local (si existe)
        rep_value, local_value = self.replace_critical(dict_in)
        rep_value = self.rounding(
            rep_value,
            operator=dict_in["operator"],
            environ=format_table["environ"],
        )
        if rep_value is None:
            return None

        local_desc = ""
        if local_value is not None:
            local_value = self.rounding(
                local_value,
                operator=dict_in["operator"],
                environ=format_table["environ"],
            )
            if local_value is not None and local_value != rep_value:
                local_desc = (
                    f" (localement {local_value} {self.units(dict_in['units'])})"
                )

        # description textuelle de la valeur
        value_desc = f"{rep_value} {self.units(dict_in['units'])}{local_desc}"

        # description textuelle de l'accumulation
        _, accum, _ = split_var_name(var_name=var_name)
        if accum > 0:
            value_desc = f"{value_desc} en {accum} h"

        if case == "short":
            return f"{self.indef_article} {self.pheno} de {value_desc}"
        return value_desc


class FFBuilder(RepresentativeValueBuilder):
    """
    Classe spécifique pour le vent
    """

    pheno = "vent"
    def_article = "le"
    indef_article = "un"
    feminin = False
    intro_var = "le vent moyen"
    var_d = "un vent moyen"

    def rounding(self, x: float, **kwargs) -> str:
        """
        Fonction pour arrondir les valeurs à l'intervalle de 5 le plus proche.
        Exemples:
            Input --> Output
             42   -->  40 à 45
             39   -->  35 à 40
        """
        if super().rounding(x, **kwargs) is None:
            return None
        start = (int(x / 5)) * 5
        stop = (int(x / 5)) * 5 + 5
        return f"{start} à {stop}"


class TemperatureBuilder(RepresentativeValueBuilder):
    """
    Classe spécifique pour la température
    """

    pheno = "température"
    def_article = "la"
    indef_article = "une"
    feminin = True

    def rounding(self, x: float, operator: str = "<", **kwargs) -> str:
        """
        On prend la valeur inférieure ou supérieur selon les cas.
        """
        if operator in ("<", "<=", "inf", "infegal"):
            return str(int(np.floor(x)))
        else:
            return str(int(np.ceil(x)))


class FFRafBuilder(RepresentativeValueBuilder):
    """
    Classe spécifique pour le vent
    """

    pheno = "rafales"
    def_article = "les"
    indef_article = "des"
    feminin = True

    environ_list = ["de l'ordre de"]

    template_retriever = read_file(
        TEMPLATES_FILENAMES[Settings().language]["multizone"]["rep_val_FFRaf"]
    )

    def rounding(self, x: float, **kwargs) -> str:
        """
        Foncion pour arrondir les valeurs à l'intervalle de  5 le plus proche.
        Exemples:
            Input --> Output
             42   -->  40 à 45
             39   -->  35 à 40
        """
        if super().rounding(x, **kwargs) is None:
            return None
        start = (int(x / 10)) * 10
        stop = (int(x / 10)) * 10 + 10
        to = "à"
        if kwargs.get("environ") == "comprises entre":
            to = "et"
        return f"{start} {to} {stop}"


class SnowBuilder(RepresentativeValueBuilder):
    """
    Classe spécifique pour la neige
    """

    pheno = "potentiel de neige"
    def_article = "le"
    indef_article = "un"
    feminin = False

    def get_variable_intro(self, variable: str) -> str:
        """
        Récupère la manière de parler de la variable
        """
        intro = super().get_variable_intro(variable)
        return f"{intro} sur {self.get_accum(variable)}"

    def get_variable_d(self, variable: str) -> str:
        """
        Récupère la manière de parler de la variable bis
        """
        intro = super().get_variable_d(variable)
        return f"{intro} sur {self.get_accum(variable)}"

    def identify_case(self, variable: str, dict_in: dict):
        (speak, format_table, local_plain, local_mountain) = super().identify_case(
            variable, dict_in
        )
        if format_table.get("value") is None:
            speak = "mountain"
        elif format_table.get("mountain_value") is None:
            speak = "plain"
        return (speak, format_table, local_plain, local_mountain)

    def add_variable_value(self, variable: str, dict_in: dict):
        """
        Pour la variable en question, on va voir si on parle que de la valeur sur
        la plaine ou  de la valeur sur la plaine et de la valeur en montagne.
        Pour l'instant la phrase est la même qu'il y ai une ou plusieurs variables.
        """
        speak, format_table, local_plain, local_mountain = self.identify_case(
            variable, dict_in
        )
        # On va maitnenant faire un arbre de décision pour savoir le type de
        # phrase à charger.
        if (
            speak == "plain"
            and local_plain is None
            and format_table["value"] is not None
        ):
            sentence_type = "plain"
        elif (
            speak == "plain"
            and local_plain is not None
            and format_table["value"] is not None
        ):
            sentence_type = "local_plain"
        elif (
            speak == "mountain"
            and format_table["mountain_value"] is not None
            and local_mountain is None
        ):
            sentence_type = "mountain"
        elif (
            speak == "mountain"
            and format_table["mountain_value"] is not None
            and local_mountain is not None
        ):
            sentence_type = "local_mountain"
        elif (
            speak == "plain_mountain" and local_plain is None and local_mountain is None
        ):
            sentence_type = "plain_mountain"
        elif (
            speak == "plain_mountain"
            and local_plain is not None
            and local_mountain is None
        ):
            sentence_type = "local_plain_mountain"
        elif (
            speak == "plain_mountain"
            and local_plain is None
            and local_mountain is not None
        ):
            sentence_type = "plain_local_mountain"
        elif (
            speak == "plain_mountain"
            and local_plain is not None
            and local_mountain is not None
        ):
            sentence_type = "local_plain_local_mountain"
        else:
            sentence_type = None

        if sentence_type is not None:
            sentence = self.get_sentence(variable, sentence_type)
            sentence = sentence.format(**format_table)
        else:
            sentence = ""
            LOGGER.error(
                "Pour la neige, on ne tombe pas dans un bon cas. Revoir pourquoi."
            )
        return sentence

    def rounding(self, x: float, **kwargs) -> str:
        """
        Foncion pour arrondir les valeurs à l'intervalle de  5 le plus proche.
        Exemples:
            Input --> Output
             42   -->  40 à 45
             39   -->  35 à 40
        """
        if super().rounding(x, **kwargs) is None:
            return None
        elif x < 1:
            return "0 à 1"
        elif x < 3:
            return "1 à 3"
        elif x < 5:
            return "3 à 5"
        elif x < 7:
            return "5 à 7"
        elif x < 10:
            return "7 à 10"
        elif x < 15:
            return "10 à 15"
        elif x < 20:
            return "15 à 20"
        start = (int(x / 10)) * 10
        stop = (int(x / 10)) * 10 + 10
        return f"{start} à {stop}"


class PrecipBuilder(RepresentativeValueBuilder):
    """
    Classe spécifique pour les précipitations
    """

    feminin = False

    def get_variable_intro(self, variable):
        """
        Récupère la manière de parler de la variable
        """
        prefix, _, _ = split_var_name(variable)
        if prefix == "PRECIP":
            return f"le cumul de précipitation sur {self.get_accum(variable)}"
        elif prefix == "EAU":
            return f"le cumul de pluie sur {self.get_accum(variable)}"
        LOGGER.error(f"Prefix unknown. Get {prefix}")

    def get_variable_d(self, variable):
        """
        Récupère la manière de parler de la variable bis
        """
        prefix, _, _ = split_var_name(variable)
        if prefix == "PRECIP":
            return f"un cumul de précipitation sur {self.get_accum(variable)}"
        elif prefix == "EAU":
            return f"un cumul de pluie sur {self.get_accum(variable)}"
        LOGGER.error(f"Prefix unknown. Get {prefix}")

    def rounding(self, x: float, **kwargs) -> str:
        """
        Foncion pour arrondir les valeurs à l'intervalle de  5 le plus proche.
        Exemples:
            Input --> Output
             42   -->  40 à 45
             39   -->  35 à 40
        """
        if super().rounding(x, **kwargs) is None:
            return None
        elif x < 3:
            return "au maximum 3"
        elif x < 7:
            return "3 à 7"
        elif x < 10:
            return "7 à 10"
        elif x < 15:
            return "10 à 15"
        elif x < 20:
            return "15 à 20"
        elif x < 25:
            return "20 à 25"
        elif x < 30:
            return "25 à 30"
        elif x < 40:
            return "30 à 40"
        elif x < 50:
            return "40 à 50"
        elif x < 60:
            return "50 à 60"
        elif x < 80:
            return "60 à 80"
        elif x < 100:
            return "80 à 100"
        start = (int(x / 50)) * 50
        stop = (int(x / 50)) * 50 + 50
        return f"{start} à {stop}"


class AltitudeBuilder(SnowBuilder):
    """
    Classe spécifique pour la neige
    """

    feminin = False

    template_retriever = read_file(
        TEMPLATES_FILENAMES[Settings().language]["multizone"]["rep_val_snow_bertrand"]
    )

    def identify_case(self, dict_in: dict) -> Tuple[str, dict]:
        """_summary_

        Args:
            variable (str): _description_
            dict_in (dict): _description_

        Returns:
            Tuple[str, dict]: _description_
        """
        format_table = {
            "pheno": self.pheno,
            "environ": self.environ(),
            "altitude": next(
                (
                    var_dict.get("mountain_altitude")
                    for var_dict in dict_in.values()
                    if "mountain_altitude" in var_dict
                ),
                0,
            ),
        }

        sorted_vars = sorted(
            [(v, *split_var_name(v)) for v in dict_in], key=lambda x: x[2]
        )

        # On regarde le nombre de prefixe de variables différent
        var_prefixes = set(v[1] for v in sorted_vars)
        case = "short"  # par défaut on enumera les noms de variables et leurs valeurs
        if len(var_prefixes) == 1:
            # s'il n'y a qu'un type de variable, on enumera juste les valeur
            case = "value"

        value_builder = None

        for stage in ("plain", "mountain"):
            var_desc_list = []
            for var, prefix, _, _ in sorted_vars:
                stage_var_dict = dict_in[var].get(stage)
                if stage_var_dict is None:
                    continue
                if prefix == "FF":
                    value_builder = FFBuilder()
                elif prefix == "RAF":
                    value_builder = FFRafBuilder()
                elif prefix == "T":
                    value_builder = TemperatureBuilder()
                elif prefix in ["PRECIP", "EAU"]:
                    value_builder = PrecipBuilder()
                elif prefix == "NEIPOT":
                    value_builder = SnowBuilder()
                else:
                    LOGGER.error(
                        "We don't know how to speak about this parameter.",
                        prefix=prefix,
                        var_name=var,
                    )
                    continue
                if value_builder is not None:
                    var_desc = value_builder.add_short_description(
                        var,
                        stage_var_dict,
                        case,
                    )
                if var_desc is not None:
                    var_desc_list.append(var_desc)

            if value_builder is not None and value_builder.pheno is not None:
                format_table["pheno"] = value_builder.pheno

            if len(var_desc_list) == 1:
                format_table[stage] = var_desc_list[0]
            elif len(var_desc_list) > 1:
                format_table[stage] = ", ".join(var_desc_list[:-1])
                format_table[stage] += f" et {var_desc_list[-1]}"

        return format_table

    def add_variable_value(self, variable: str, dict_in: dict) -> str:
        """
        Pour la variable en question, on va voir si on parle que de la valeur sur
        la plaine ou  de la valeur sur la plaine et de la valeur en montagne.
        Pour l'instant la phrase est la même qu'il y ai une ou plusieurs variables.
        """
        format_table = self.identify_case(dict_in)
        sentence = ""
        if "plain" in format_table:
            sentence += "{pheno} sous {altitude} m: {plain}. "
        if "mountain" in format_table:
            sentence += "{pheno} au-dessus de {altitude} m: {mountain}."
        return sentence.format(**format_table)
