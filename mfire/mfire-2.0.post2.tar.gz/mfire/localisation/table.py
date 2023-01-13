"""
This module is for the management of 3x3 tables.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any, Iterable, Optional, Tuple, Sequence, Union
import dateutil


import xarray as xr
import numpy as np

from mfire.localisation import SpatialIngredient, rename_alt_min_max, compute_IoU
from mfire.text.period_describer import PeriodDescriber
from mfire.utils.date import Datetime, Period
from mfire.utils.json_utils import JsonFile
from mfire.settings import get_logger, ALT_MIN, ALT_MAX

# Logging
LOGGER = get_logger(name="table.mod", bind="table")

# to be put in internalization files
JOINER = " et "

xr.set_options(keep_attrs=True)


def get_representative_area_properties(
    area_list: xr.DataArray,
    area_possibilities: xr.DataArray,
    domain: xr.DataArray = None,
    alt_min: Optional[int] = ALT_MIN,
    alt_max: Optional[int] = ALT_MAX,
) -> Tuple[str, str]:
    """
    On va essayer de trouver la zone qui represente le mieux l'union
    de area_list afin de nommer la liste.
    S'il n'y a pas de candidats idéal, on va s'occuper de renommer
    (brutalement) certaines propriétés.
    Fonction utilisée dans le résumé.

    Args:
        area_list (dataArray): La liste d'entrée des zones à fusionner
        area_possibilities (dataArray): Les possibilités de fusion
        domain (dataArray) : Le domaine utilisé dans les calculs.
            Pour s'appeler avec le nom du domaine la condition est plus stricte.

    Returns:
        [Tuple]: [Le nom de la zone, le type de la zone]
    """
    area_sum = area_list.sum("id", min_count=1)
    IoU = compute_IoU(area_sum, area_possibilities)
    IoUMax = IoU.max("id")
    a_max = IoU.argmax("id")
    LOGGER.debug(f"Maximum of IoU for area merge {IoUMax.values}")
    if IoUMax > 0.6:
        area_name = area_possibilities.isel(id=a_max).areaName.values
        area_type = area_possibilities.isel(id=a_max).areaType.values
    else:
        list_name = area_list["areaName"].values.astype(str)
        list_name.sort()
        area_name = JOINER.join(list_name)
        if area_name.count(JOINER) > 1:
            area_name.replace(JOINER, ", ", area_name.count(JOINER) - 1)
        if len(np.unique(area_list.areaType)) == 1:
            area_type = area_list.areaType[0]
        else:
            area_type = "No"
    # On test aussi avec l'ensemble du domaine s'il existe
    if domain is not None:
        IoU = compute_IoU(area_sum, domain)
        LOGGER.debug(f"IoU for domain is {IoU.values}")
        if IoU > 0.98:
            area_name = domain["areaName"].values
            area_type = "domain"

    area_name = rename_alt_min_max(
        area_name=area_name,
        alt_min=alt_min,
        alt_max=alt_max,
    )

    LOGGER.debug(f"Name : {str(area_name)}, Type: {str(area_type)}")
    return (str(area_name), str(area_type))


def bin_to_int(sequence: Sequence[Any]) -> int:
    """Encode a given iterable containing binary values to an integer.

    For instances:
    >>> bin_to_int([1, 0, 1])
    5
    >>> bin_to_int("110")
    6

    Args:
        sequence: (Sequence): Sequence to encode

    Returns:
        int: encoded sequence
    """
    return int("".join(str(int(v)) for v in sequence), base=2)


def encode_table(table_da: xr.DataArray, dim: str = "id") -> Tuple:
    """Encode a 2-D binary DataArray into a tuple of integer along the dimension dim.

    For instance:
    >>> da = xr.DataArray(
    ...     [[1, 1, 0], [0, 1, 1]],
    ...     coords=(("id", ["a", "b"]), ("period", ["p0", "p1", "p2"])),
    ... )
    >>> encode_table(da)
    (6, 3)

    Args:
        table_da (xr.DataArray): Table to encode.
        dim (str, optional): Dimension to apply encoding along to. Defaults to "id".

    Raises:
        ValueError: raised if values in the table_da DataArray are not convertible
            to int.

    Returns:
        Tuple: Encoded table.
    """
    try:
        return tuple([bin_to_int(table_da.sel({dim: v}).values) for v in table_da[dim]])
    except ValueError as excpt:
        LOGGER.error(
            "Failed to encode table along given dim. Exception Raised.",
            table_da=table_da,
            dim=dim,
        )
        raise excpt


def define_raw_table_name(raw_table: Iterable[Union[str, int]]) -> str:
    """
    Retourne le nom correspondant à partir d'une liste/tuple
    en base 10 (incluant un string pour la période).Le nom est générique.
    Ainsi les lignes sont triées de la plus petite à la plus grande dans
    la fonction.

    Args:
        raw_table (Iterable[Union[str, int]]): Le tableau à résumé.
            Par exemple ["3",7,2,0]

    Returns:
        str: Le nom du talbeau
    """
    base = [next(k for k in raw_table if isinstance(k, str))]
    nums = sorted(str(int(k)) for k in raw_table if not isinstance(k, str))
    return f"P{'_'.join(base + nums)}"


class SummarizedTable:
    """
    Gere les tableaux résumant la situation.
    """

    _nc_table = "input_table.nc"
    _spatial_base_name = "SpatialIngredient"
    _json_config = "summarized_table_config.json"

    def __init__(
        self,
        da: xr.DataArray,
        request_time: Datetime,
        full_period: Period,
        spatial_ingredient: Optional[SpatialIngredient] = None,
    ):
        """
        Args:
            da (DataArray): A 3 period dataArray
            request_time (Datetime) : production datetime
            full_period (Period) : periode couverte par le bulletin
                Permettrait de mettre en relief le tableau.
        """
        self.input_table = da
        self.spatial_ingredient = spatial_ingredient
        self.request_time = request_time
        self.full_period = full_period
        # ------------------------------------
        self.period_describer = PeriodDescriber(request_time)

        self.working_table = da.copy()

        self.unique_table = xr.Dataset()
        self.unique_name = "Unknown"
        self.define_unique_table()

    def auto_save(self, fname: Path):
        """Permet la sauvegarde des éléments pour les recharger.

        Args:
            fname (Path): Nom de base
        """
        fname = Path(fname)
        LOGGER.info(f"Saving  summarized table to {fname / self._nc_table}")
        self.input_table.to_netcdf(fname / self._nc_table)
        if self.spatial_ingredient is not None:
            self.spatial_ingredient.auto_save(fname / self._spatial_base_name)
        # On va aussi sauver un fichier json contenant request_time et full_period
        dout = {}
        dout["request_time"] = self.request_time
        dout["full_period"] = self.full_period.toJson()
        JsonFile(fname / self._json_config).dump(dout)

    @classmethod
    def load(cls, fname: Path) -> SummarizedTable:
        """Enable to load a SummarizedTable element saved with auto_save method.

        Args:
            fname (Path): The same path/basename [description]

        Returns:
            [type]: [description]
        """
        fname = Path(fname)
        input_table = xr.open_dataarray(fname / cls._nc_table).load()
        if (fname / cls._spatial_base_name).exists():
            spatial_ingredient = SpatialIngredient.load(fname / cls._spatial_base_name)
        else:
            spatial_ingredient = None
        data = JsonFile(fname / cls._json_config).load()
        request_time = data["request_time"]
        full_period = Period(**data["full_period"])
        return cls(input_table, request_time, full_period, spatial_ingredient)

    def get_unique_table(self) -> xr.DataArray:
        """Return table. The table is sorted and in reduced form
        Returns:
            [dataArray]: The table
        """
        return self.unique_table

    def get_unique_name(self) -> str:
        """Return the name of the reduced form table

        Returns:
            [str]: The table name
        """
        return self.unique_name

    def get_raw_table(self) -> list:
        """Return reduced table as a list

        Returns:
            [list]: The list contain  the number of period
                    as well as the description of each table line.
        """
        return self.raw_table

    def check_unique(self) -> bool:
        """
        Permet de voir si le tableau est bien sous forme "unique".
        Les règles de permutations doivent être respectées pour les lignes
        Sur les colonnes, les règles doivent aussi être respectées.
        Cependant on ne peut pas vérifier qu'elles sont dans le "bon ordre".
        On peut juste vérifier que :
           - la première et dernière colonne n'est pas vide
        """
        result = True
        code = encode_table(self.unique_table)
        l_code = sorted(code)
        if l_code != list(code):
            LOGGER.warning(
                f"Line are not correctly sorted. {code}. Should be ascending order."
            )
            result = False
        if len(set(code)) != len(code):
            LOGGER.warning(f"Redundant line exists {code}.")
            result = False
        if self.unique_table.isel(period=0).sum() == 0:
            LOGGER.warning(f"First column has no risk {self.unique_table}")
            result = False
        if self.unique_table.isel(period=-1).sum() == 0:
            LOGGER.warning(f"Last column has no risk {self.unique_table}")
            result = False
        return result

    def define_unique_table(self) -> None:
        """
        This function perform operation on the input table.
         - Squeeze empty period
         - merge similar period
         - Order and merge area
        This is done while keeping information on AreaName and on PeriodName.
        It enable to define the "unique_table" and the unique_name
        """
        self.squeeze_empty_period()
        self.merge_similar_period()
        self.merge_period_with_same_name()
        self.merge_similar_period()

        # Il va falloir maintenant permuter les lignes
        raw_table = list(encode_table(self.working_table))
        self.working_table["raw"] = (("id"), raw_table)
        raw_table.insert(0, str(int(self.working_table.period.size)))
        self.raw_table = raw_table
        self.unique_name = define_raw_table_name(frozenset(raw_table))
        # On va permuter et fusionner les lignes en fonction des résultats du tuple
        # On n'a pas besoin de redefinir le nom unique apres
        # (on sait avant de l'envoyer au charbon qu'il y aura fusion)
        self.unique_table = self.order_and_merge_area()[self.input_table.name]

    def squeeze_empty_period(self) -> None:
        """
        Supprime les périodes vides en début et fin de talbeau.
        """
        i = 0
        squeeze_list = []
        while self.working_table.isel(period=[i]).sum().values == 0:
            squeeze_list.append(i)
            i += 1
        i = self.working_table.period.size - 1
        while self.working_table.isel(period=[i]).sum().values == 0:
            squeeze_list.append(i)
            i += -1
        select = set([i for i in range(self.working_table.period.size)])
        to_select = sorted(select.difference(set(squeeze_list)))
        self.working_table = self.working_table.isel(period=to_select)

    def merge_similar_period(self) -> None:
        """
        Merge similar period.
        Two period are similar if they are adjacent and risk values are the same.

        This function should work for any number of period.
        """
        if self.working_table.period.size > 0:
            index_to_remove = []
            period_name = [self.working_table.period.isel(period=0).values]
            for p in range(1, self.working_table.period.size):
                if (
                    self.working_table.isel(period=[p]).values
                    == self.working_table.isel(period=[p - 1]).values
                ).all():
                    index_to_remove.append(p)
                    # Mettre un nom de period en adequation.
                    period_name[-1] = (
                        str(period_name[-1])
                        + "_+_"
                        + str(self.working_table.isel(period=[p])["period"].values[0])
                    )
                else:
                    period_name.append(self.working_table.period.isel(period=p).values)
        if index_to_remove != []:
            index = set(list(range(self.working_table.period.size)))
            index = index.difference(set(index_to_remove))
            keep_list = sorted(index)
            self.working_table = self.working_table.isel(period=keep_list)
            self.working_table["period"] = period_name

    def merge_period_with_same_name(self) -> None:
        """Permet de merger des periodes qui auraient le meme nom.

        Returns:
            None
        """
        # On va commencer par juste afficher les périodes
        array_name = self.working_table.name
        the_names = []
        for period in self.working_table["period"].values:
            time_list = period.split("_to_")
            try:
                period_obj = Period(time_list[0], time_list[-1])
                LOGGER.debug(
                    f"Period = {period_obj} "
                    f"({self.period_describer.describe(period_obj)})"
                )
            except dateutil.parser._parser.ParserError:
                LOGGER.warning(
                    f"At least one period value is not a datetime {period}. "
                    "We will not merge period by name."
                )
                return None
            the_names += [self.period_describer.describe(period_obj)]

        self.working_table["period_name"] = (("period"), the_names)
        # Maintenant on va merger
        # Pour cela on va selectionner les periodes ayant le même nom et on les merge.
        # On suppose que des périodes portent le même nom seulement si elles sont
        # consécutives.
        if len(set(the_names)) != len(the_names):
            LOGGER.info(
                "Différentes périodes ont le même nom. "
                "On va merger ces périodes (en prenant le pire des risques)."
            )
            tmp_list = []
            # LOGGER.info(f"Nom des périodes {the_names}")
            for pname in set(the_names):
                table_to_reduce = self.working_table.where(
                    self.working_table.period_name == pname, drop=True
                )
                if table_to_reduce.period.size > 1:
                    reduced_table = table_to_reduce.max("period")
                    first_period = str(
                        table_to_reduce["period"].isel(period=0).values
                    ).split("_to_")
                    last_period = str(
                        table_to_reduce["period"].isel(period=-1).values
                    ).split("_to_")
                    # On va vérifier
                    reduced_pname = self.period_describer.describe(
                        Period(first_period[0], last_period[-1])
                    )
                    if pname != reduced_pname:
                        LOGGER.info(
                            f"After merging similar period named {pname}, "
                            f"the period_name is different: {reduced_pname}"
                        )
                    reduced_table["period"] = first_period[0] + "_to_" + last_period[-1]
                    reduced_table = reduced_table.expand_dims("period")
                    tmp_list += [reduced_table]
                else:
                    tmp_list += [table_to_reduce]
            self.working_table = xr.merge(tmp_list)[array_name]
        if "period_name" in self.working_table.coords:
            self.working_table = self.working_table.drop_vars("period_name")
        return None

    def merge_zones(
        self,
        da: xr.DataArray,
        alt_min: Optional[int] = ALT_MIN,
        alt_max: Optional[int] = ALT_MAX,
    ) -> xr.DataArray:
        """
        Devrait fonctionner avec n'importe quel nombre de zones
        Merge les zones similaires.
        Conserve les autres variables dépendant de l'identificateur de zones

        Devrait être appelé depuis l'exterieur pour merger des zones du talbeau ?

        Args :
            da (DataArray)
        """
        if da["id"].size > 1:
            dout = xr.Dataset()
            # Determination du nouvel id
            area_id = "_+_".join(da["id"].values.astype(str))
            dout = da.isel({"id": 1})

            dout = (
                dout.drop_vars("id").expand_dims("id").assign_coords({"id": [area_id]})
            )
            # On va regarder les autres coordonnées.
            # On merge de manière pas bête les noms seulement si on a un
            # spatial_ingredient.
            if "areaName" in da.coords and self.spatial_ingredient is not None:
                ids_set = {v for ids in da.id.values for v in ids.split("_+_")}
                sel_ids_set = ids_set.intersection(
                    self.spatial_ingredient.localised_area.id.values
                )
                if sel_ids_set != ids_set:
                    LOGGER.warning(
                        "Ids non présents dans localised_area",
                        missing_ids=list(ids_set.difference(sel_ids_set)),
                        ids_set=list(ids_set),
                        id_localised=self.spatial_ingredient.localised_area.id.values,
                    )
                (area_name, area_type) = get_representative_area_properties(
                    self.spatial_ingredient.localised_area.sel(id=list(sel_ids_set)),
                    self.spatial_ingredient.full_area_list,
                    domain=self.spatial_ingredient.domain,
                    alt_min=alt_min,
                    alt_max=alt_max,
                )
                dout["areaName"] = ("id", [str(area_name)])
                dout["areaType"] = ("id", [area_type])
                LOGGER.debug(f"areaName {area_name} ")
            elif "areaName" in da.coords:
                dout["areaName"] = (
                    "id",
                    [
                        "_+_".join(
                            rename_alt_min_max(
                                area_name=da["areaName"].values.astype(str),
                                alt_min=alt_min,
                                alt_max=alt_max,
                            )
                        )
                    ],
                )
                dout["areaType"] = (("id"), ["mergedArea"])

        else:
            dout = da
            if "areaName" in da.coords:
                dout["areaName"] = (
                    "id",
                    [
                        rename_alt_min_max(
                            area_name=da.areaName.values[0],
                            alt_min=alt_min,
                            alt_max=alt_max,
                        )
                    ],
                )
        return dout

    def order_and_merge_area(self) -> xr.DataArray:
        """
        Ordonne le dataArray pour être en phase avec le modèle unique.
        Fusionne aussi les zones similaires.
        Returns :
           Le dataArray avec les zones mergées et permutées.
        """

        dout = xr.Dataset()
        table = sorted(set(self.working_table["raw"].values))
        final_list = []
        area_list = []  # Permet d'etre sur de l'ordre apres le merge.
        for elt in table:
            db = self.working_table.sel({"id": (self.working_table["raw"] == elt)})
            dtmp = self.merge_zones(db.drop_vars("raw"))
            area_list.append(dtmp["id"].values[0])
            final_list.append(dtmp)

        dout = xr.merge(final_list).sel({"id": area_list})
        if "areaName" in dout.coords:
            dout["areaName"] = dout["areaName"].astype(str)
        return dout

    def update_uniqueTable(self, id_list: list) -> None:
        """Updates the self.unique_table by selecting given ids.

        Args:
            id_list (list): List of ids to select in the self.unique_table.
        """
        LOGGER.debug(f"Unique_name before {self.unique_name}")
        area_to_merge = self.working_table.sel(id=id_list)
        merged_area = self.merge_zones(area_to_merge)
        unmerged_id = [
            idi for idi in self.working_table.id.values if idi not in id_list
        ]
        unmerged_area = []
        if unmerged_id != []:
            unmerged_area = self.working_table.sel(id=unmerged_id)
            self.working_table = xr.merge(
                [merged_area.drop_vars("raw"), unmerged_area.drop_vars("raw")]
            )["elt"]
        else:
            self.working_table = merged_area.drop_vars("raw")
        self.define_unique_table()
        LOGGER.debug(f"Unique_name after {self.unique_name}")


if __name__ == "__main__":
    df = xr.Dataset()
    df.coords["period"] = [
        "20190727T06_to_20190727T11",
        "20190727T12_to_20190727T14",
        "20190727T15_to_20190727T16",
    ]
    #   df.coords["zone"] = [f"zone{k+1}" for k in range(3)]
    df.coords["id"] = [
        "4830b20e-e936-4e65-9bf2-737dd451275c",
        "24830b20e-e936-4e65-9bf2-737dd451275cd",
        "34830b20e-e936-4e65-9bf2-737dd451275ce",
    ]
    df["elt"] = (("id", "period"), [[0, 1, 0], [0, 1, 0], [1, 0, 1]])
    df["areaName"] = (("id"), ["Area1", "Area2", "Area3"])

    df = df.swap_dims({"id": "areaName"}).swap_dims({"areaName": "id"})
    Full_period = Period("20190726T16", "20190727T15")
    Request_time = "20190726T16"
    table_handler = SummarizedTable(
        df["elt"], request_time=Request_time, full_period=Full_period
    )
    table_handler.auto_save("/scratch/labia/chabotv/test")
    print(table_handler.get_unique_name())
    print(table_handler.get_unique_table())

    new_table = SummarizedTable.load("/scratch/labia/chabotv/test")
    print(new_table.get_unique_table())
    print(new_table.full_period)
