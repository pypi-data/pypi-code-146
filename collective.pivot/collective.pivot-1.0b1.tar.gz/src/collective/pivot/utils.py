# -*- coding: utf-8 -*-
from plone import api
from zope.i18n import translate


def _(msgid, context, domain="collective.pivot", mapping=None):
    return translate(msgid, context=context.REQUEST, mapping=mapping)


def add_family(context, family_id, title):
    """Add a family in the configuration folder"""
    Family = api.content.create(
        container=context, type="collective.pivot.Family", family=family_id, title=title
    )
    return Family
