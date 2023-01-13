from mfire.settings import get_logger
from mfire.localisation.localisation_manager import Localisation
from mfire.localisation.core_spatial import LocalisationError

import xarray as xr
import numpy as np
from pydantic import BaseModel
from typing import Dict, List, Union
from mfire.composite import RiskComponentComposite
from mfire.composite.operators import ComparisonOperator
from mfire.utils.date import Datetime
from mfire.settings import MONOZONE, TEMPLATES_FILENAMES
from mfire.text.template import CentroidTemplateRetriever, read_file
from mfire.text.comment.multizone import ComponentHandlerLocalisation

# Logging
LOGGER = get_logger(name="text_reducer.mod", bind="text_reducer")


class Reducer(BaseModel):
    """Reducer :  Objet gérant toutes les fonctionnalités du composant
    nécessaires à la création d'un commentaire approprié.
    """

    module: str = "monozone"
    component: RiskComponentComposite
    reduction: Dict = {}

    def reset(self) -> None:
        """Initialise la réduction en dicionnaire vide"""
        self.reduction = dict()

    def compute(self, geo_id: str, component: RiskComponentComposite) -> None:
        """
        Permet de décider quel module de génération de commentaire est à utiliser.

        Args:
            geo_id (str): Id de la zone.
            component (RiskComponentComposite): composant étudié
        """
        maxi_risk = component.get_final_risk_max_level(geo_id)

        if maxi_risk >= 1:
            # Mettre d'autres conditions pour ne pas passer par la localisation.
            #   - Type de risque (upstream/downstream)

            # On recupere la définition du risque
            risk_list = component.select_risk_level(level=maxi_risk)

            agg = risk_list[0].aggregation_type

            if agg == "downStream":
                hourly_maxi_risk = component.final_risk_da.sel(id=geo_id)
                # On recupere la periode où le risque le plus grand existe
                risk_period = hourly_maxi_risk.sel(
                    valid_time=(hourly_maxi_risk == maxi_risk)
                ).valid_time
                try:
                    # TODO refact de ComponentHandlerLocalisation
                    # ou de Localisation à prévoir
                    self.reduction = ComponentHandlerLocalisation(
                        localisation_handler=Localisation(
                            component,
                            risk_level=maxi_risk,
                            geo_id=geo_id,
                            period=set(risk_period.values),
                        )
                    )
                    unique_table, _ = self.reduction.get_summarized_info()
                    # On va regarder s'il est nécessaire de faire de
                    # la localisation spatiale sur le risque le plus eleve.
                    if unique_table.id.size > 1:
                        self.module = "multizone"
                        LOGGER.debug("Going to multiZone commentary type")
                        return None

                except LocalisationError as e:
                    # Si c'est une erreur 'normale' du module de localisaion
                    # (pas de zones descriptive, pas le bon type de risque, etc... ).
                    # On passe alors au module monozone.
                    LOGGER.warning(repr(e))

        # On est dans le cas par défault -> monozone
        self.reduce_monozone(geo_id)

    def get_operator_dict(self) -> dict:
        """pour récupérer les opérateurs de comparaisons
        (utilisés pour les arrondis des valeurs représentatives)

        Returns:
            operator_dict (dict): dictionnaire contenant
            les operateurs de comparaison par evenement
        """
        operator_dict = dict()
        for level in self.component.levels:
            for ev in level.elements_event:
                operator_dict[ev.field.name] = {"plain": ev.plain.comparison_op}
                try:
                    operator_dict[ev.field.name]["mountain"] = ev.mountain.comparison_op
                except AttributeError:
                    pass
        return operator_dict

    def get_rep_value(self, values: List, operator: ComparisonOperator) -> float:
        """en fonction de l'opérateur de comparaison,
        cette fonction renvoie la valeur représentative

        Args:
            values (list): liste des valeurs représentatives pour chaque échéance
            operator (ComparisonOperator): opérateur de comparaison

        Returns:
            la valeur représentative
        """
        if operator in (
            ComparisonOperator.SUP,
            ComparisonOperator.SUPEGAL,
        ):
            return max(values)
        elif operator in (
            ComparisonOperator.INF,
            ComparisonOperator.INFEGAL,
        ):
            return min(values)
        else:
            LOGGER.warning(
                f"get_rep_value:cas non connu {operator}",
                func="get_representative_values",
            )
            return np.NaN

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

    def get_template_type(self, bloc: dict, reduced_risk: List) -> None:
        """On recherche le type de template (general, snow ou precip)
        - si le niveaux max est de type différent du niveau intermédiaire => general
        - si seul niveau max est activé => on regarde les evenements :
            pluie + pluie = pluie
            neige + neige = neige
            neige + pluie = pluie/neige
            autres : general

        Args:
            bloc (dict): bloc de la reduction
            reduced_risk (list) : risk réduits
        """

        bloc_copy = {
            k: v
            for k, v in bloc.items()
            if k not in ["level", "start", "stop", "centroid_value"]
        }

        if max(reduced_risk) == bloc["level"]:
            evs = set()
            for ev in bloc_copy.keys():
                if "PRECIP" in ev or "EAU" in ev:
                    evs.add("PRECIP")
                elif "NEIPOT" in ev:
                    evs.add("SNOW")
                else:
                    evs.add(ev)

            if evs == {"PRECIP"}:
                self.reduction["type"] = "PRECIP"
            elif evs == {"SNOW"}:
                self.reduction["type"] = "SNOW"
            elif evs == {"PRECIP,SNOW"}:
                self.reduction["type"] = "PRECIP_SNOW"
            else:
                self.reduction["type"] = "general"

    def process_value(
        self, param: str, events: List, operator_dict: dict, ev_type: str
    ) -> dict:
        """recupére toutes les valeurs significatives min, max, val rep, units ..
        pour plain ou mountain (argument ev_type).

        Args:
            param (str): parametre ex NEIPOT24__SOL
            events (list): liste de dataset contenant les events pour un param
            operator_dict (dict): dictionnaire contant les opérateurs de comparaisons
            ev_type (str): plain ou mountain

        Returns:
            dict: dictionnaire contenant les informations ou None si on a pas les infos
            (cas d'un paramètre qualificatif
            ou quand ev_type = mountain lorsqu'on n'a pas de mountain)
        """

        vars = events[0].data_vars
        min_v = np.NaN
        max_v = np.NaN
        rep_value = np.NaN
        units = np.NaN
        operator = np.NaN

        if (
            "min_" + ev_type in vars
            and "max_" + ev_type in vars
            and "rep_value_" + ev_type in vars
            and ev_type in operator_dict[param]
        ):
            # ex : si on a un param qualificatif (ex WWMF) on ne rentre pas dans ce if
            ev_values = []
            units = []
            for ev in events:

                if ev["min_" + ev_type].values < min_v or np.isnan(min_v):
                    min_v = ev["min_" + ev_type].values

                if ev["max_" + ev_type].values > max_v or np.isnan(max_v):
                    max_v = ev["max_" + ev_type].values

                ev_values.append(ev["rep_value_" + ev_type].values)

            units = str(events[0].units.values)

            rep_value = self.get_rep_value(
                values=ev_values, operator=operator_dict[param][ev_type]
            )

            operator = operator_dict[param][ev_type]

        values_dict = {
            "min": None if (min_v == "nan" or np.isnan(min_v)) else float(min_v),
            "max": None if (max_v == "nan" or np.isnan(max_v)) else float(max_v),
            "value": None
            if (rep_value == "nan" or np.isnan(rep_value))
            else float(rep_value),
            "units": units,
            "operator": operator,
        }

        if None in values_dict.values() and ev_type == "mountain":
            return None
        return values_dict

    def get_infos(self, data: List) -> dict:
        """permet de récupérer les infos pour chaque bloc Bi

        Args:
            data (list): list de data array (pour le level == 0)
                         OU de dataset d'un même niveau

        Returns:
            bloc (dict): dictionnaire résumant les informations voulues
        """
        bloc = dict()

        if isinstance(data[0], xr.DataArray):
            bloc["level"] = 0
            time = [ech.values for ech in data]
            bloc["start"] = Datetime(min(time))
            bloc["stop"] = Datetime(max(time))
        else:
            operator_dict = self.get_operator_dict()
            event_dict = dict()
            time = list()

            # on regroupe par evenement

            for ech in data:
                time.append(ech.valid_time.values)
                for ev in ech.evt:
                    event = ech.sel(evt=ev)
                    key_event = str(event.weatherVarName.values)
                    if key_event != "nan":
                        if key_event in event_dict.keys():
                            event_dict[key_event].append(event)
                        else:
                            event_dict[key_event] = [event]

            for k, v in event_dict.items():
                if k != "nan":
                    bloc[k] = dict()

                    plain = self.process_value(k, v, operator_dict, "plain")
                    bloc[k]["plain"] = {**plain}

                    mountain = self.process_value(k, v, operator_dict, "mountain")
                    if bool(mountain):
                        bloc[k]["mountain"] = {**mountain}

            bloc["level"] = int(data[0].risk_level.values)
            bloc["start"] = Datetime(min(time))
            bloc["stop"] = Datetime(max(time))

        return bloc

    def reduce_risk(
        self, final_risk: xr.DataArray, component: xr.Dataset
    ) -> Union[List, dict]:
        """Reduit le risque en blocs en fonction des blocs retrouvés après utilisation de la dtw

        Args:
            final_risk (dataarray): risque
            component (dataset) : composant étudié ici, qui contient
                                les informations à extraire dans la réduction

        Returns:
            reduced_risk (list): risque réduit en un vecteur
            reduction (dict): dictionnaire contenant les informations pour chaque bloc
            exemple : reduction = {
                "B0": {
                    "level" : 0,
                    "start" : "2021-02-01T09:00:00",
                    "stop" : "2021-02-01T14:00:00",
                    "centroid_value" : 0
                },
                "B1" : {
                    "level" : 2,
                    "start" : "2021-02-01T15:00:00",
                    "stop" : "2021-02-01T20:00:00",
                    "RAF__HAUTEUR10" : {
                        "plain" : {
                            ...
                        },
                    },
                    "FF__HAUTEUR10" : {
                        "plain" : {
                            ...
                        },
                        "mountain" : {
                            ...
                        }
                    },
                    "centroid_value" : 1
                },

                "production_datetime" : ,
                "risk_max" : 2
            }
        """
        # pour chaque échéance on rajoute le numéro de bloc et la valeur du centroid
        final_risk["blocks"] = ("valid_time", [v[1] for v in self.reduction["path"]])

        centroid_list = list()
        last = final_risk["blocks"].values[0]

        for x in final_risk["blocks"].values:
            if last == x:
                centroid_list.append(self.reduction["centroid"][last])

            else:
                centroid_list.append(self.reduction["centroid"][last + 1])
            last = x

        final_risk["centroid"] = ("valid_time", centroid_list)
        reduced_risk = list()

        actives_levels = component["risk_level"].values

        reduction = self.reduction
        previous_centroid = final_risk["centroid"].values[0]
        previous_block = final_risk["blocks"].values[0]
        same_level_list = list()

        for i, level in enumerate(final_risk):
            if i == len(final_risk) - 1:
                # on gère le dernier élément de la liste
                if previous_centroid != level["centroid"].values:
                    # on termine par un centroid différent ex : [1,1,1,0.75]
                    reduction["B" + str(previous_block)] = self.get_infos(
                        same_level_list
                    )
                    reduction["B" + str(previous_block)][
                        "centroid_value"
                    ] = previous_centroid
                    if level["centroid"].values == 0:
                        reduction["B" + str(level["blocks"].values)] = self.get_infos(
                            [level["valid_time"]]
                        )
                    elif level.values in actives_levels:
                        reduction["B" + str(level["blocks"].values)] = self.get_infos(
                            [
                                component.sel(
                                    valid_time=level["valid_time"],
                                    risk_level=level.values,
                                )
                            ]
                        )

                    reduction["B" + str(level["blocks"].values)][
                        "centroid_value"
                    ] = level["centroid"].values

                else:
                    # on termine par un centroid identique ex : [1,1,1,0.75,0.75]
                    if level["centroid"].values == 0:
                        same_level_list.append(level["valid_time"])
                    elif level.values in actives_levels:
                        same_level_list.append(
                            component.sel(
                                valid_time=level["valid_time"],
                                risk_level=level.values,
                            )
                        )

                    reduction["B" + str(previous_block)] = self.get_infos(
                        same_level_list
                    )
                    reduction["B" + str(previous_block)][
                        "centroid_value"
                    ] = previous_centroid
                break
            elif previous_centroid == level["centroid"].values:
                # tant qu'on est dans le même bloc consécutif on garde les infos
                # dans une même liste ex : 1 -> 1
                if level["centroid"].values == 0:
                    same_level_list.append(level["valid_time"])

                elif level.values in actives_levels:
                    same_level_list.append(
                        component.sel(
                            valid_time=level["valid_time"],
                            risk_level=level.values,
                        )
                    )

                previous_centroid = level["centroid"].values
                previous_block = level["blocks"].values
            else:
                # au changement de bloc on récupère les infos
                # dans un bloc de la réduction ex : 1 -> 2
                reduction["B" + str(previous_block)] = self.get_infos(same_level_list)
                same_level_list = list()
                if level["centroid"].values == 0:
                    same_level_list.append(level["valid_time"])

                elif level.values in actives_levels:
                    same_level_list.append(
                        component.sel(
                            valid_time=level["valid_time"],
                            risk_level=level.values,
                        )
                    )

                reduction["B" + str(previous_block)][
                    "centroid_value"
                ] = previous_centroid
                previous_centroid = level["centroid"].values
                previous_block = level["blocks"].values

        reduced_risk = [v["level"] for k, v in reduction.items() if isinstance(v, dict)]
        reduction["reduced"] = reduced_risk
        reduction["compo_hazard"] = str(
            self.component.name + "_" + self.component.hazard_name
        )
        reduction["production_datetime"] = self.component.production_datetime

        return reduced_risk, reduction

    def compare_val(self, max_val: dict, level: int, data: dict, key: str) -> bool:
        """pour comparer les valeurs representatives
        de plain ou, si elles sont égales, de mountain

        Args:
            max_val (dict): param plus haute valeur représentative actuellement
            level (int): niveau
            data (dict): data à comparer
            key (str): paramètre (ex EAU1__SOL)

        Returns:
            bool: true si la valeur dans max est la plus grande, false sinon
        """

        operators = self.get_operator_dict()

        if self.compare_worst(
            max_val[level][key]["plain"]["value"],
            data["plain"]["value"],
            operators[key]["plain"],
        ):
            return True
        elif max_val[level][key]["plain"]["value"] == data["plain"]["value"]:
            try:
                return self.compare_worst(
                    max_val[level][key]["mountain"]["value"],
                    data["mountain"]["value"],
                    operators[key]["mountain"],
                )
            except (AttributeError, KeyError):
                return True
        else:
            return False

    def get_levels_val(self) -> None:
        """Rajoute dans la reduction des information sur les niveaux max et int
        pour cela on compare les valeurs représentatives
        d'un même param pour un même niveau
        """

        max_val = {"level_max": dict(), "level_int": dict()}

        for bloc, data in self.reduction.items():
            if bloc.startswith("B"):
                data_copy = {
                    k: v
                    for k, v in data.items()
                    if k not in ["level", "start", "stop", "centroid_value"]
                }
                if data["centroid_value"] == 1:
                    for key, param in data_copy.items():
                        if key in max_val["level_max"] and self.compare_val(
                            max_val, "level_max", param, key
                        ):
                            pass
                        else:
                            max_val["level_max"][key] = param

                elif data["level"] == 0:
                    pass
                else:
                    for key, param in data_copy.items():
                        if key in max_val["level_int"] and self.compare_val(
                            max_val, "level_int", param, key
                        ):
                            pass
                        else:
                            max_val["level_int"][key] = param
        for level, data in max_val.items():
            self.reduction[level] = data

    def compute_distance(self, norm_risk: List, method="random"):
        """recherche dans la matrice monozone pour détermier le template
        à l'aide de la dtw on trouve la distance la plus faible

        Args:
            norm_risk (list): niveaux de risques normalisés
            methode (str): first, random ou last (default)

           on rajoute à la réduction les infos du centroid choisi :
           {
               "distance": ,
               "path": ,
               "template" : ,
               "centroid" : ,
               "type" :
           }
        """
        template_retriever = CentroidTemplateRetriever.read_file(
            MONOZONE, index_col=["0", "1", "2", "3", "4"]
        )
        self.reduction.update(
            template_retriever.get_by_dtw(norm_risk, pop_method=method)
        )

    def reduce_monozone(self, geo_id: str) -> None:
        """Permet de réduire l'information pour le cas monozone
        en se ramenenant à un seul vecteur

        Args:
            geo_id (str): id de la zone
        """

        self.reset()

        final_risk = self.component.final_risk_da.sel(id=geo_id)
        component = self.component.risks_ds.sel(id=geo_id)

        risk_max = max(final_risk.values)
        risk_min = min(final_risk.values)
        level_max = max(self.component.risks_ds.risk_level.values)

        # on normalise les niveaux de risques
        norm_risk = final_risk.values
        if level_max > 1:
            norm_risk = np.where(
                norm_risk, 1 - (((level_max - norm_risk) * 0.5) / (level_max - 1)), 0
            )

        # on utilise la dtw pour se raprocher d'un template
        self.compute_distance(norm_risk=norm_risk)

        # on réduit le risque en blocs
        reduced_risk, self.reduction = self.reduce_risk(final_risk, component)
        self.reduction["risk_max"] = risk_max
        self.reduction["risk_min"] = risk_min
        self.reduction["level_maxi"] = level_max

        self.get_levels_val()

        # on cherche le type de template
        for key, bloc in self.reduction.items():
            if key.startswith("B"):
                if bloc["level"] == risk_max and bloc["level"] != 0:
                    self.get_template_type(bloc, reduced_risk)

        if self.reduction["type"] != "general":
            template_retriever = read_file(
                TEMPLATES_FILENAMES["fr"]["monozone"]["precip"]
            )
            default = (
                "Echec dans la récupération du template"
                f"(key={self.reduction['type']}) (error COM-001)."
            )
            self.reduction["template"] = template_retriever.get(
                key=self.reduction["type"], default=default
            )
