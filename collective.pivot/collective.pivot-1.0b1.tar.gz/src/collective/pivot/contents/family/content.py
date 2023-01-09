# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from collective.pivot import _


class IFamily(model.Schema):
    """Marker interface for Family"""

    family = schema.Choice(
        title=_(u"Pivot family"),
        required=True,
        vocabulary="collective.pivot.vocabularies.Families",
    )
    zip_codes = schema.List(
        title=_(u"Zip codes"),
        description=_(
            u"Leave empty if you want to get zip codes from global settings."
        ),
        value_type=schema.TextLine(title=_(u"Zip code")),
        required=False,
    )


@implementer(IFamily)
class Family(Container):
    """Pivot Family container class"""
