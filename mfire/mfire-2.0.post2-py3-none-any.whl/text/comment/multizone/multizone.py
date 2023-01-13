"""
@package text.comment.multizone

Module retrieving text templates
"""

# Standard packages
from __future__ import annotations

# Own package
from mfire.settings import Settings, TEMPLATES_FILENAMES
from mfire.text.comment.multizone.comment_builder import (
    TemplateCommentBuilder,
    PeriodCommentBuilder,
    ZoneCommentBuilder,
)
from mfire.text.comment.representative_builder import RepresentativeValueManager
from mfire.text.comment.multizone import ComponentInterface
from mfire.text.template import read_file
from mfire.utils.text_tools import (
    start_sentence_with_capital,
    modify_unit,
)
from mfire.settings import get_logger

# Logging
LOGGER = get_logger(name="text.comment.multizone.mod", bind="text.comment.multizone")


def new_multizone(template_name, monozone_access=None) -> MultiZone:
    """new_multizone: temporary function that creates a full MultiZone
    CommentBuilder out of the box.

    Returns:
        Multizone: new multizone comment builder object.
    """
    key = "generic"
    if template_name == "SNOW":
        key = "snow"
    elif template_name == "PRECIP":
        key = "precip"
    return MultiZone(
        read_file(TEMPLATES_FILENAMES[Settings().language]["multizone"][key]),
        monozone_access=monozone_access,
    )


class MultiZone(
    TemplateCommentBuilder,
    PeriodCommentBuilder,
    ZoneCommentBuilder,
    RepresentativeValueManager,
):
    """Multizone: specific CommentBuilder for handling 'multizone' types of
    components.

    Args:
        template_retriever (TemplateRetriever): Object that is able to find and
            provide a template corresponding to the self.component_handler.

    Inheritance:
        TemplateCommentBuilder
        PeriodCommentBuilder
        ZoneCommentBuilder
    """

    def handle_area_problems(self, areaIds) -> None:
        LOGGER.debug(f"Fonction permettant de gérer les erreurs de zones {areaIds}")
        # 1. On va devoir faire modifier le template
        self.component_handler.modify_template(areaIds)
        LOGGER.debug(
            f"Template après modif {self.component_handler.get_template_key()}"
        )
        # 2. On refait tourner le template_retriever
        self.retrieve_template()
        # 3. On reprocess les periodes
        self.process_period()
        # 4. On refait les zones
        self.process_zone(self.handle_area_problems)
        # La cinquième étape est réalisée suite au précédent process_zone
        # (ayant appellé handle_area_problems).

    def compute(self, component_handler: ComponentInterface) -> None:
        """process: method for processing a full self.text according to the
        given component_handler.

        Args:
            component_handler (ComponentHandler): Object handling all the component's
                features necessary to create an appropriate comment.

        """
        self.reset()
        self.component_handler = component_handler
        self.retrieve_template()
        self.process_period()
        self.process_zone(self.handle_area_problems)
        self.process_value()

        return modify_unit(start_sentence_with_capital(self.text))
