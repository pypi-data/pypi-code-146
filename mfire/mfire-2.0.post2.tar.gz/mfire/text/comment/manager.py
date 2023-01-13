import xarray as xr
from pydantic import BaseModel
from typing import Optional, Any
from functools import partial

from mfire.settings import get_logger
from mfire.composite import RiskComponentComposite

from mfire.text.comment.multizone import new_multizone
from mfire.text.comment import Reducer
from mfire.text.comment.monozone import Monozone


# Logging
LOGGER = get_logger(name="manager.mod", bind="manager")

xr.set_options(keep_attrs=True)


class Manager(BaseModel):
    """Module permettant de gérer la génération de commentaires.
    C'est dans ce module qu'on va décider vers quel module de
    génération de texte on va orienter."""

    selector: Any
    reducer: Optional[Reducer]
    builder: Any

    def build_monozone(self, component: RiskComponentComposite, geo_id: str) -> str:
        """Permet de générer le commentaire pour un type monozone

        Args:
            component (RiskComponentComposite): composant risk étudié
            geo_id (str): id de la zone

        Returns:
            str: le commentaire détaillé
        """

        self.reducer.reduce_monozone(geo_id)
        self.builder = Monozone(self.reducer.reduction["template"])

        comment = self.builder.compute(self.reducer.reduction)

        return comment

    def compute(
        self,
        geo_id: str,
        component: RiskComponentComposite,
    ) -> str:
        """
        Permet de récupérer le commentaire pour la zone identifiée
        Attention cette fonction a besoin que decision_tree ai été déclenché auparavant.

        Args:
            geo_id (str) : L'identifiant de la zone

        Returns:
            str: Le commentaire
        """
        self.reducer = Reducer(component=component)
        self.reducer.compute(geo_id, component)

        if self.reducer.module == "monozone":
            self.builder = Monozone(self.reducer.reduction["template"])
        else:
            template_name = self.reducer.reduction.get_template_type()
            self.builder = new_multizone(
                template_name,
                monozone_access=partial(self.build_monozone, geo_id=geo_id),
            )

        return self.builder.compute(self.reducer.reduction)
