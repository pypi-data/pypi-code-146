from enum import unique
from django.contrib.postgres.fields import ArrayField
from django.db import models
from netbox.models import NetBoxModel, ChangeLoggedModel
from django.urls import reverse
from netbox.models.features import WebhooksMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Risk(NetBoxModel):
    name = models.CharField(
        max_length=250,
        unique=False
    )

    firstname = models.CharField(
        max_length=250,
        blank=True,
    )
    lastname = models.CharField(
        max_length=250,
        blank=True,
    )

    ENABLED = 'enabled'
    DISABLED = 'disabled'
    DELETED = 'deleted'
    NEEDACTION = 'need action'

    CHOICES = (
        (ENABLED, ENABLED),
        (DISABLED, DISABLED),
        (DELETED, DELETED),
        (NEEDACTION, NEEDACTION),
    )

    status = models.CharField(
        max_length=250,
        unique=False,
        choices=CHOICES,
        default=ENABLED
    )

    sAMAccountName = models.CharField(
        max_length=250,
        unique=True,
        blank=False,
    )

    ad_guid = models.CharField(
        max_length=250,
        blank=True,
    )

    vpnIPaddress = models.CharField(
        max_length=250,
        blank=True,
    )
    ad_description = models.CharField(
        max_length=250,
        blank=True,
    )
    position = models.CharField(
        max_length=250,
        blank=True,
    )
    department = models.CharField(
        max_length=250,
        blank=True,
    )
    comment = models.CharField(
        max_length=250,
        blank=True,
    )

    description = models.CharField(
        max_length=500,
        blank=True,
    )
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:users_and_computers:aduser', args=[self.pk])


class RiskRelation(NetBoxModel):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    CN = models.CharField(
        max_length=250,
        unique=True,
        blank=False,
    )

    DistinguishedName = models.CharField(
        max_length=500,
        unique=True,
        blank=False,
    )

    ad_guid = models.CharField(
        max_length=250,
        blank=True,
    )

    ad_description = models.CharField(
        max_length=500,
        blank=True,
    )

    description = models.CharField(
        max_length=500,
        blank=True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        # return 'reskrel'
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:users_and_computers:riskrelation', args=[self.pk])


