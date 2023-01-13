import numpy as np
import shapely.geometry as geom

from mfire.configuration.geos import FeatureCollectionConfig
from mfire.utils import JsonFile
from mfire.utils.geo import CompassRose8, distance_on_earth
from mfire.text.base import BaseBuilder
from mfire.sit_gen import SynObj
from mfire.text.template import read_file
from mfire.settings import get_logger, TEMPLATES_FILENAMES, SIT_GEN


TPL = read_file(TEMPLATES_FILENAMES["fr"]["situation_generale"])

# Logging
LOGGER = get_logger(name="sitgen_builder.mod", bind="sitgen_builder")


def get_threshold(pname: str, thresh_name: str, is_max: bool = False) -> int | None:
    """Returns the thresholds contained in SIT_GEN[pname] dictionnary.

    Args:
        pname (str): Name given in the properties.
        thresh_name (str): Name of the threshold.
        is_max (bool, optional): Whether to use the max value or not.

    Returns:
        dict[str, tuple[str, str]]: Thresholds.
    """
    return SIT_GEN.get(pname, dict()).get(thresh_name, (None, None))[is_max]


class SitGenBuilder(BaseBuilder):
    """
    Builder spécifique pour gérer les textes de situation générale

    Inheritance:
        BaseBuilder
    """

    mouvement: str
    prevision: str
    is_zone_geo: bool
    info_sup: str
    qualification: str
    position: str

    def get_name(self, pname: dict, pmer: int = 0, associe: bool = False) -> str:
        """Returns the full textual name of the synoptic object.

        Args:
            pname (dict): Name given in the properties.
            pmer (int, optional): Value of the sea level pressure, given in the
                properties as the "value_pmer". Defaults to 0.
            associe (bool, optional): Whether the given object is a associated front.
                Defaults to False.

        Returns:
            str: Textual name.
        """
        if pname == "depression" and pmer >= 1015:
            return TPL.get(("names", "relative"))
        name = next(v for k, v in TPL.table["names"].items() if k == pname)
        return TPL.get("associe").format(name=name) if associe else name

    def build_position(self, pname: str, point_coords: tuple[float, float]) -> None:
        """Assign the textual description of the position given by the point_coords.

        Args:
            pname (str): Name given in the properties.
            point_coords (tuple[float, float]): Coordinates of the point to describe.
        """
        # Initiate Point as a Feature Config
        point = geom.Point(point_coords)

        # Creating zones to compare with
        filename = next(f for k, f in SIT_GEN["zones"].items() if k in pname)
        zones = FeatureCollectionConfig(**JsonFile(filename).load()).features

        # Finding Best Zone
        best_zone = min(
            ((zone.shape.distance(point), zone.shape.area, zone) for zone in zones),
            key=lambda x: x[:2],
        )[2]

        # Finding direction according to an in-box
        zone_bounds = np.array(best_zone.shape.bounds).reshape((2, 2))
        inbox = geom.box(*np.dot([[0.75, 0.25], [0.25, 0.75]], zone_bounds).flatten())
        direction = "default"
        if not inbox.contains(point):
            direction = CompassRose8.from_points(
                best_zone.shape.centroid.coords[0],
                point_coords,
            ).name
        pre = best_zone.properties["prefixes"]
        self.position = (
            pre.get(direction, pre["default"]) + best_zone.properties["label"]
        )

    def build_qualification(self, pname: str, val0: int, val1: int, meme_previ: bool):
        """Assign the proper qualification adjective to the self.qualification.

        Args:
            pname (str): Name given in the properties.
            val0 (int): First representative value.
            val1 (int): Second representative value.
            meme_previ (bool): If the second prevision is similar to the first one.
        """
        fast_thresh = get_threshold(pname, "fast", meme_previ)
        slow_thresh = get_threshold(pname, "slow", meme_previ)
        evol_thresh = get_threshold(pname, "evol", meme_previ)

        self.qualification = ""
        if any(v is None for v in (fast_thresh, slow_thresh, evol_thresh)):
            return None

        if abs(val0 - val1) >= fast_thresh:
            self.qualification = TPL.get("fast")
        elif evol_thresh < abs(val0 - val1) <= slow_thresh:
            self.qualification = TPL.get("slow")

    def build_mouvement(
        self, pname: str, val0: int, val1: int, deplacement: int, meme_previ: bool
    ):
        """Assign the movement adjective to the self.mouvement

        Args:
            pname (str): Name given in the porperties
            val0 (int): First representative value.
            val1 (int): Second representative value.
            deplacement (int): Shift distance in kilometers.
            meme_previ (bool): If the second prevision is similar to the first one.
        """
        evol_thresh = get_threshold(pname, "evol", meme_previ)
        move_thresh = get_threshold(pname, "move", meme_previ)

        if abs(val0 - val1) <= evol_thresh:
            self.mouvement = TPL.get("slow_move")
            if deplacement >= move_thresh:
                self.mouvement = TPL.get("shift")
        elif val0 < val1:
            self.mouvement = TPL.get(("increase", pname))
        else:
            self.mouvement = TPL.get(("decrease", pname))

    @staticmethod
    def modify_vocab(input: str) -> str:
        """Replace stop words in the given geographical name.

        Args:
            zone_geo (str): name to change

        Returns:
            str: Name with replaced stop words.
        """
        output = input
        for old, new in TPL.table.get("replace", dict()).items():
            output = output.replace(old, new)
        return output

    def build_prevision(
        self,
        pname: str,
        val0: int,
        val1: int,
        deplacement: int,
        direction: str,
        zone_geo: str,
        last_previ: bool,
        meme_previ: bool,
    ):
        """Assign the forecasted representative value to the self.prevision.

        Args:
            pname (str): Name given in the properties.
            val0 (int): First representative value.
            val1 (int): Second representative value.
            deplacement (int): Shift distance in kilometers.
            direction (str): Direction of the object's movement.
            zone_geo (str): Name of the position of the object.
            last_previ (bool): If the given preivision is the last one.
            meme_previ (bool): If the second prevision is similar to the first one.
        """

        evol_thresh = get_threshold(pname, "evol", meme_previ)
        move_thresh = get_threshold(pname, "move", meme_previ)

        self.is_zone_geo = False
        tpl = TPL.get(("forecast", "base"))

        if abs(val0 - val1) <= evol_thresh:
            tpl = ""
            if deplacement >= move_thresh:
                if last_previ:
                    tpl = TPL.get(("forecast", "direction"))
                else:
                    self.is_zone_geo = True
                    tpl = TPL.get(("forecast", "position"))

        self.prevision = tpl.format(
            planned=TPL.get(("planned", pname)),
            value=val1,
            direction=direction,
            position=self.modify_vocab(zone_geo),
        )

    @staticmethod
    def quand(last_previ: bool):
        if last_previ:
            return TPL.get("end")
        return TPL.get("later")

    def build_infoSup(
        self,
        pname: str,
        val0: int,
        val1: int,
        deplacement: int,
        direction: str,
        position2: str,
        last_previ: bool,
        meme_previ: bool,
    ):
        """Assign additional informations to the self.info_sup attribute.

        Args:
            pname (str): Name given in the properties.
            val0 (int): First representative value.
            val1 (int): Second representative value.
            deplacement (int): Shift distance of the objectif.
            direction (str): Direction of the object's movement.
            position2 (str): Name of the next position.
            last_previ (bool): If the given preivision is the last one.
            meme_previ (bool): If the second prevision is similar to the first one.
        """

        evol_thresh = get_threshold(pname, "evol", meme_previ)
        move_thresh = get_threshold(pname, "move", meme_previ)

        txt1 = " " + position2
        txt2 = " " + self.quand(last_previ)
        self.build_prevision(
            pname,
            val0,
            val1,
            deplacement,
            direction,
            position2,
            last_previ,
            meme_previ,
        )

        if "depression" in pname:
            if abs(val0 - val1) > evol_thresh:
                info_sup = txt1
                if deplacement < move_thresh:
                    info_sup = TPL.get("stationary")
                info_sup += txt2

        elif "anticyclone" == pname:
            info_sup = txt1 + txt2

        if abs(val0 - val1) <= evol_thresh:
            info_sup = "."
            if deplacement >= move_thresh:
                info_sup = txt1 + txt2
                if self.is_zone_geo:
                    info_sup = txt2

        self.info_sup = info_sup

    def process_ad(
        self,
        pname: str,
        val0: int,
        val1: int,
        pt0: tuple[float, float],
        pt1: tuple[float, float],
        last_previ: bool,
        meme_previ: bool,
    ) -> None:
        """Method made for processing a anticyclone or depression sentence.

        Args:
            pname (str): Name given in the properties
            val0 (int): First representative value.
            val1 (int): Second representative value.
            pt0 (list): Coordinates of the first position
            pt1 (list): Coordinates of the second position
            last_previ (bool): If the given preivision is the last one.
            meme_previ (bool): If the second prevision is similar to the first one.
        """
        deplacement = distance_on_earth(pt0, pt1)
        self.build_mouvement(pname, val0, val1, deplacement, meme_previ)
        self.build_qualification(pname, val0, val1, meme_previ)
        direction = CompassRose8.from_points(pt0, pt1).text
        self.build_position(pname, pt1)
        self.build_prevision(
            pname,
            val0,
            val1,
            deplacement,
            direction,
            self.position,
            last_previ,
            meme_previ,
        )
        self.build_infoSup(
            pname,
            val0,
            val1,
            deplacement,
            direction,
            self.position,
            last_previ,
            meme_previ,
        )

    def compute_fronts(self, l_final: list, associe: bool = False) -> str:
        """Texte pour un objet de type front"""

        text = ""
        tpl = TPL.get(key="fronts", default="Failed to retrieve front template")

        for l_objs in l_final:
            properties = l_objs[0]["properties"]
            self.build_position(
                properties["name"],
                SynObj(**l_objs[0]).shape.centroid.coords[0],
            )
            text += (
                tpl.format(
                    name=self.get_name(
                        properties["name"],
                        properties.get("value_pmer"),
                        associe=associe,
                    ),
                    position=self.position,
                    direction=l_objs[0]["properties"]["direction"],
                )
                + "\n"
            )

        return text

    def compute_ad(self, l_final: list) -> str:
        """Texte pour un objet dépression ou anticyclone"""

        text = ""
        tpl = TPL.get(key="ad", default="Failed to retrieve AD template")

        for l_objs in l_final:
            pname = l_objs[0]["properties"]["name"]
            val_0h = l_objs[0]["properties"]["value_pmer"]

            if "depression" in pname or (pname == "anticyclone" and val_0h > 1015):
                # tambouille bizarre pour trouver l'échéance 12h après le début
                # on prend le 4 élément de la liste (car on a des pas de 3H) si
                # la liste contient plus de 4 éléments, sinon on prend le dernier
                k_12h = 4 if len(l_objs) > 4 else -1
                val_12h = l_objs[k_12h]["properties"]["value_pmer"]
                pt_12h = l_objs[k_12h]["geometry"]["coordinates"]

                meme_previ = False
                last_previ_12h = True

                mouvement_24h = ""
                qualification_24h = ""
                prevision_24h = ""
                info_sup_24h = ""

                if len(l_objs) >= 7:
                    last_previ_12h = False
                    last_previ_24h = True

                    val_24h = l_objs[-1]["properties"]["value_pmer"]
                    pt_24h = l_objs[-1]["geometry"]["coordinates"]

                    self.process_ad(
                        pname,
                        val_12h,
                        val_24h,
                        pt_12h,
                        pt_24h,
                        last_previ_24h,
                        meme_previ,
                    )

                    mouvement_24h = TPL.get("then") + self.mouvement
                    qualification_24h = self.qualification
                    prevision_24h = self.prevision
                    info_sup_24h = self.info_sup

                pt_0h = l_objs[0]["geometry"]["coordinates"]

                self.process_ad(
                    pname, val_0h, val_12h, pt_0h, pt_12h, last_previ_12h, meme_previ
                )

                mouvement_12h = self.mouvement
                qualification_12h = self.qualification
                prevision_12h = self.prevision
                info_sup_12h = self.info_sup

                if mouvement_12h == mouvement_24h[7:]:
                    meme_previ = True
                    self.process_ad(
                        pname,
                        val_0h,
                        val_24h,
                        pt_0h,
                        pt_24h,
                        last_previ_24h,
                        meme_previ,
                    )

                    mouvement_12h = self.mouvement
                    qualification_12h = self.qualification
                    prevision_12h = self.prevision
                    info_sup_12h = self.info_sup
                    mouvement_24h = ""
                    qualification_24h = ""
                    prevision_24h = ""
                    info_sup_24h = ""

                self.build_position(pname, pt_0h)
                text += (
                    tpl.format(
                        name=self.get_name(pname, val_0h),
                        value=val_0h,
                        position=self.position,
                        mouvement_12h=mouvement_12h,
                        qualification_12h=qualification_12h,
                        prevision_12h=prevision_12h,
                        info_sup_12h=info_sup_12h,
                        mouvement_24h=mouvement_24h,
                        qualification_24h=qualification_24h,
                        prevision_24h=prevision_24h,
                        info_sup_24h=info_sup_24h,
                    )
                    + "\n"
                )

        return text

    def compute(self, reduction: dict) -> None:
        """
        Texte de situation générale complet
        """

        if list(reduction.values()) == [[], [], [], []]:
            self._text = TPL.get("RAS")
        else:
            self._text = ""
            for depr_fr in reduction["joined_depressions_fronts"]:
                self._text += self.compute_ad([depr_fr[0]])
                self._text += self.compute_fronts([depr_fr[1]], associe=True)

            self._text += self.compute_ad(reduction["depressions"])
            self._text += self.compute_ad(reduction["anticyclones"])
            self._text += self.compute_fronts(reduction["fronts"])
