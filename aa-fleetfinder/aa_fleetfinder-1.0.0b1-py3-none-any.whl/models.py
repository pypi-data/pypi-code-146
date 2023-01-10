"""
Models
"""

# Django
from django.db import models

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter
from allianceauth.groupmanagement.models import AuthGroup


class General(models.Model):
    """
    General module permissions
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta Definitions
        """

        verbose_name = "Fleet Finder"
        managed = False
        default_permissions = ()
        permissions = (
            ("access_fleetfinder", "Can access the Fleet Finder app"),
            ("manage_fleets", "Can manage fleets"),
        )


class Fleet(models.Model):
    """
    Fleet Model
    """

    fleet_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    fleet_commander = models.ForeignKey(
        EveCharacter,
        on_delete=models.SET_NULL,
        related_name="fleetfinder_fleet_commander",
        default=None,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField()
    motd = models.TextField(blank=True, default="")
    is_free_move = models.BooleanField()

    groups = models.ManyToManyField(
        AuthGroup,
        related_name="fleetfinder_restricted_groups",
        help_text="Groups listed here will be able to join the fleet",
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta Definitions
        """

        default_permissions = ()
