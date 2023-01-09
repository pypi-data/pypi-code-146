# -*- coding: utf-8 -*-
"""Init and utils."""
from plone import api
from zope.i18nmessageid import MessageFactory

HAS_PLONE_5_AND_MORE = api.env.plone_version().startswith('5') or api.env.plone_version().startswith('6')

_ = MessageFactory("collective.pivot")
