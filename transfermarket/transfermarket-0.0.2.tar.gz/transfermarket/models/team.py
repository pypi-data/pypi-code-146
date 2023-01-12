"""
This module contains the domain model for Team.
"""
from transfermarket.models.meta import MetaModel


class Team(MetaModel):
    """
    This class contains the model for a team.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.id = kwargs.get("id")
        self.title = kwargs.get("title")
        self.abbreviation = kwargs.get("abbreviation")

    def __repr__(self):
        """
        This method returns a string representation of the team.
        """
        avps = []

        if self.id is not None:
            avps.append(f"id='{self.id}'")

        avps.append(f"title='{self.title}'")

        return f"<Team({', '.join(avps)})>"
