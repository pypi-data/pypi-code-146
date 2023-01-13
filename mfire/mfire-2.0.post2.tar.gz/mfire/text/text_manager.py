from typing import Union, Optional

from pydantic import BaseModel

from mfire.settings import get_logger
from mfire.composite.components import RiskComponentComposite, TextComponentComposite
from mfire.text.comment import Manager

from mfire.text.factory import DirectorFactory


LOGGER = get_logger(name="text_manager.mod", bind="text_manager")


class TextManager(BaseModel):
    """Class for dispatching the text generation according to the given component's
    type.

    Args:
        component (Union[RiskComponentComposite, TextComponentComposite]) :
            Component to produce a text with.
    """

    component: Union[RiskComponentComposite, TextComponentComposite]
    _reduction: Optional[dict] = None  # temporary reduction attr for sit_gen usage

    class Config:
        """Cette classe Config permet de contrôler de comportement de pydantic"""

        underscore_attrs_are_private = True

    def compute_sit_gen(self, geo_id: str = None) -> str:
        """Temporary method for producing the

        Args:
            geo_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        # It is really really bad practice to import elsewhere than the top of the file
        # BUT one of those imports depends on TensorFlows/Keras end is sloooooooow
        # (We are talking ~5s load time, it basically doubles the compute time of a
        # component). Since the ovewhelming majority of the productions dont need
        # those imports, we skip them until we need them and our HPC cpu use time
        # is cut in half. If someone got a better way to do this, fell free to do so :)
        from mfire.text.sit_gen import SitGenReducer, SitGenBuilder

        if self._reduction is None:
            self._reduction = SitGenReducer().compute(self.component)
        builder = SitGenBuilder()
        builder.compute(self._reduction[geo_id])
        return builder._text

    def compute(self, geo_id: str = None) -> str:
        """Produce a text according to the given self.component's type.

        Args:
            geo_id (str, optional): Optional geo_id for comment generation.
                Defaults to None.

        Returns:
            str: Text corresponding to the self.component and the given GeoId.
        """
        if isinstance(self.component, TextComponentComposite):
            if all(w.id.startswith("sitgen") for w in self.component.weathers):
                return self.compute_sit_gen(geo_id=geo_id)

            my_text = ""
            for weather in self.component.weathers:
                director = DirectorFactory()
                my_text += director.compute(weather=weather) + "\n"
            return my_text

        manager = Manager()
        return manager.compute(geo_id=geo_id, component=self.component)
