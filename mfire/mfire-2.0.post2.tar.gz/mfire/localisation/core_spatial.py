import copy
from typing import Optional, Tuple

import numpy as np
import xarray as xr

from mfire.settings import (
    get_logger,
    ALT_MIN,
    ALT_MAX,
    SPACE_DIM,
    TIME_DIM,
    N_CUTS,
    GAIN_THRESHOLD,
    Dimension,
)
from mfire.localisation.area_algebre import RiskArea

__all__ = ["get_n_area"]

# Logging
LOGGER = get_logger(name="localisation", bind="localisation")

np.warnings.filterwarnings("ignore")


class LocalisationError(ValueError):
    pass


def get_variance(
    risk_da: xr.DataArray,
    area_da: xr.DataArray,
    space_dim: Dimension = SPACE_DIM,
    time_dim: Dimension = TIME_DIM,
) -> xr.DataArray:
    """Calcule la variance de risk_da sur chaque zone de area_da,
    selon les dimensions spatiales et temporelles données.

    Args:
        risk_da (xr.DataArray): DataArray contenant le risque préalablement calculé.
        area_da (xr.DataArray): DataArray contenant un ensemble de zones.
        space_dim (Dimension): Dimension(s) spatiale(s).
            Defaults to SPACE_DIM.
        time_dim (Dimension): Dimension(s) temporelle(s).

    Returns:
        xr.DataArray: DataArray donnant listant la variance du risque zone par zone.
    """
    return (area_da * risk_da).var(space_dim).sum(time_dim) * area_da.sum(space_dim)


def best_separation(
    risk_da: xr.DataArray,
    area_handler: RiskArea,
    domain_da: xr.DataArray,
    space_dim: Dimension = SPACE_DIM,
    time_dim: Dimension = TIME_DIM,
) -> Tuple[xr.DataArray, xr.DataArray, float]:
    """Renvoie la meilleure séparation du domaine (domain_da) en 2 zones
    complémentaires qui minimisent la variance du risque au sein de chaque zones.

    Args:
        risk_da (xr.DataArray): DataArray contenant le risque préalablement calculé.
        area_handler (RiskArea): Object contenant la liste des zones descriptives
            possibles à utiliser.
        domain_da (xr.DataArray): Dataarray contenant le domaine.
        space_dim (Dimension): Dimension(s) spatiale(s).
            Defaults to SPACE_DIM.
        time_dim (Dimension): Dimension(s) temporelle(s).

    Returns:
        Tuple[xr.DataArray, xr.DataArray, float]: Tuple contenant les deux meilleures
            zones ainsi que le gain de variance obtenu par rapport au risque sur tout
            le domaine.
    """
    # Variance initiale (avant subdivision)
    area_da, comp_area_da = area_handler.get_possibilities(domain_da)

    if area_da is None:
        LOGGER.debug("We did not found any 'valid subdivision'")
        return None, None, -1000

    var_init_da = get_variance(risk_da, domain_da, space_dim, time_dim)

    # Calcul des variance intra pour chacune des zones
    var_area_intra_da = get_variance(risk_da, area_da, space_dim, time_dim)
    var_comp_intra_da = get_variance(risk_da, comp_area_da, space_dim, time_dim)
    var_intra_da = var_area_intra_da + var_comp_intra_da
    # On recherche le var_argmin
    var_argmin = var_intra_da.load().argmin()
    # Selection de la zone et de son complementaire
    best_area_da = area_da.isel(id=var_argmin)
    # Selection du complémentaire
    best_comp_area_da = comp_area_da.isel(id=var_argmin)
    # On change d'ID car pour l'instant il a celui du complémentaire
    best_comp_area_da["id"] = f"comp_{str(best_comp_area_da.id.values)}"
    # On calcul le gain obtenu par cette subdivision
    gain = (var_init_da - var_intra_da.isel(id=var_argmin)).values
    LOGGER.debug(
        f"gain subdivision {gain} pour de ce domaine {domain_da['areaName'].values} "
        f"en zone {area_da.isel(id=var_argmin)['areaName'].values} et ce complementaire"
        f" {comp_area_da.isel(id=var_argmin)['areaName'].values}."
    )
    return best_area_da, best_comp_area_da, gain


def get_n_area(
    risk_da: xr.DataArray,
    domain_da: xr.DataArray,
    full_list_da: xr.DataArray,
    n_cuts: Optional[int] = N_CUTS,
    gain_threshold: Optional[float] = GAIN_THRESHOLD,
    between_authorized: Optional[bool] = False,
    alt_min: Optional[int] = ALT_MIN,
    alt_max: Optional[int] = ALT_MAX,
    space_dim: Dimension = SPACE_DIM,
    time_dim: Dimension = TIME_DIM,
) -> xr.DataArray:
    """Découpe un domaine donné en n_cuts zones issues de full_list_da selon la variance
    du risque au sein de ces zones.

    Args:
        risk_da (xr.DataArray): DataArray contenant le risque préalablement calculé.
        domain_da (xr.DataArray): DataArray contenant la zone définie comme domaine.
        full_list_da (xr.DataArray): DataArray contenant la liste des zones
            descriptives valables pour effectuer le découpage.
        n_cuts (Optional[int]): Nombre de découpage successifs. Defaults to N_CUTS.
        gain_threshold (Optional[float]): Condition d'arrêt. Si on améliore la variance
            de moins de gain_threshold %, alors on ne propose pas le découpage comme
            solution. Defaults to GAIN_THRESHOLD.
        between_authorized (Optional[bool]): Autorise les zones d'altitudes dont le nom
            est "entre xxx m et yyy m". Defaults to False.
        alt_min (Optional[int], optional): Altitude min. Defaults to ALT_MIN.
        alt_max (Optional[int], optional): Altitude max. Defaults to ALT_MAX.
        space_dim (Dimension): Dimension(s) spatiale(s).
            Defaults to SPACE_DIM.
        time_dim (Dimension): Dimension(s) temporelle(s).

    Raises:
        LocalisationError: Erreur déclenchée s'il est impossible d'effectuer un seul
            découpage du domaine. Cela permet d'indiquer au TextManager que le
            monozone peut prendre le relai.

    Returns:
        xr.DataArray: DataArray contenant les zones selectionnées.
    """
    area_handler = RiskArea(
        full_list_da=full_list_da,
        between_authorized=between_authorized,
        alt_min=alt_min,
        alt_max=alt_max,
    )

    var_init_da = get_variance(risk_da, domain_da, space_dim, time_dim)

    # On cherche la premiere separation de domain_da
    #
    domain_da_copy = copy.deepcopy(domain_da)  # ? necessite du deepcopy ici
    if "id" in domain_da_copy.dims:
        domain_da_copy = domain_da_copy.squeeze("id")
    best_zone1_da, comp_best_zone1_da, _ = best_separation(
        risk_da, area_handler, domain_da_copy
    )

    if best_zone1_da is None:
        raise LocalisationError(
            f"Ce domaine ({domain_da.areaName.values}) ne peut être découpé via "
            "ses zones descriptives. Aucun couple ne peut y etre trouvé."
        )

    # On cree un dictionnaire d'area transitoire

    dict_area = {}
    dict_area[str(best_zone1_da.areaName.values)] = best_zone1_da
    dict_area[str(comp_best_zone1_da.areaName.values)] = comp_best_zone1_da
    l_pos = {}
    # On cree une liste des "areas" en sortie
    l_out_area = []
    l_out_area.append(prepare_area(best_zone1_da))
    l_out_area.append(prepare_area(comp_best_zone1_da))
    # On ajoute en possibilité la décomposition de best_zone1_da et comp_best_zone1_da
    for _ in range(1, n_cuts):
        best_zone2_da, comp_best_zone2_da, gain_zone2 = best_separation(
            risk_da, area_handler, best_zone1_da
        )
        if gain_zone2 / var_init_da > gain_threshold:
            l_pos[str(best_zone2_da.areaName.values)] = {
                "area": best_zone2_da,
                "areab": comp_best_zone2_da,
                "gain": gain_zone2,
                "parent": best_zone1_da,
            }
        elif gain_zone2 < 0:
            LOGGER.debug(
                f"Pas de subdivision valide pour {best_zone1_da.areaName.values}"
            )
        else:
            LOGGER.debug(
                f"gain trop faible {gain_zone2 / var_init_da.values} "
                f"{best_zone2_da.areaName}"
            )

        best_zone3_da, comp_best_zone3_da, gain_zone3 = best_separation(
            risk_da, area_handler, comp_best_zone1_da
        )
        if gain_zone3 / var_init_da > gain_threshold:
            l_pos[str(best_zone3_da.areaName.values)] = {
                "area": best_zone3_da,
                "areab": comp_best_zone3_da,
                "gain": gain_zone3,
                "parent": comp_best_zone1_da,
            }
        elif gain_zone3 < 0:
            LOGGER.debug(
                f"Pas de subdivision valide pour {comp_best_zone1_da.areaName.values}"
            )
        else:
            LOGGER.debug(
                f"gain trop faible {gain_zone3 / var_init_da.values} "
                f"{best_zone3_da.areaName}"
            )

        if len(l_pos) > 0:
            idi = max(l_pos, key=lambda x: l_pos[x]["gain"])
            LOGGER.debug("Zone choisie pour le redecoupage %s", idi)
            dict_to_add = l_pos.pop(idi)
            # On retire la zone indésirable
            l_out_area = [da for da in l_out_area if da.id != dict_to_add["parent"].id]
            # On redefinie la zone et son complémentaire.
            best_zone1_da = dict_to_add["area"]
            comp_best_zone1_da = dict_to_add["areab"]
            l_out_area.append(prepare_area(best_zone1_da))
            l_out_area.append(prepare_area(comp_best_zone1_da))
        else:
            # On s'arrete prematurement : les decoupages ne permettent pas de continuer
            break
    return xr.merge(l_out_area)[l_out_area[0].name]


def prepare_area(area_da: xr.DataArray) -> xr.DataArray:
    """Permet de renvoyer un dataArray avec des dimensions prêtes pour le merge.
    Args:
        area_da (DataArray): Le dataArry à modifier

    Raises:
        ValueError: Si on est pas du type dataArray

    Returns:
        [DataArray]: DataArray modifié (areaName et areaType sont des dimensions
            indexées par id)
    """
    # On va rajouter 'areaName et areaType'.
    if not isinstance(area_da, xr.core.dataarray.DataArray):
        raise ValueError("Input is expected to be a dataArray")
    name = area_da.name
    area_da = area_da.reset_coords(["areaName", "areaType"])
    if "id" not in area_da.dims:
        area_da = area_da.expand_dims("id")
    else:
        area_da["areaName"] = area_da["areaName"].expand_dims("id")
        area_da["areaType"] = area_da["areaType"].expand_dims("id")
    area_da = (
        area_da.swap_dims({"id": "areaName"})
        .swap_dims({"areaName": "areaType"})
        .swap_dims({"areaType": "id"})
    )

    return area_da[name]


if __name__ == "__main__":
    # Pour l'instant le test fonctionne uniquement chez moi ....
    # A voir s'il faut faire quelque chose de plus générique.
    import matplotlib.pyplot as plt
    from mfire.utils.xr_utils import MaskLoader

    RISK = xr.open_dataset("../../localisation/ex_riskt2m.nc")[
        "__xarray_dataarray_variable__"
    ]
    RISK = RISK.drop("areaName")
    AREA = MaskLoader(
        filename="../../localisation/GeoOut/Geo_Isère.nc",
        grid_name="eurw1s100",
    ).load()

    FULL_DOMAIN = AREA.max("id")
    FULL_DOMAIN["areaName"] = "domain"
    FULL_DOMAIN["areaType"] = "test"

    ds_loca = get_n_area(RISK, FULL_DOMAIN, AREA, gain_threshold=0.02)
    ds_loca.swap_dims({"id": "areaName"}).plot(col="areaName")
    plt.savefig("test_localisation.png")
