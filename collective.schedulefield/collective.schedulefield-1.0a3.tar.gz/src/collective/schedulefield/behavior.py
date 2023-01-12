# -*- coding: utf-8 -*-
"""
collective.schedulefield
------------------------

Created by mpeeters
:license: GPL, see LICENCE.txt for more details.
"""

from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform.view import WidgetsView
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel.directives import fieldset
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider

from collective.schedulefield import _
from collective.schedulefield.schedule import Schedule
from collective.schedulefield.schedule import ScheduleWithTitle
from collective.schedulefield.exceptionalclosure import ExceptionalClosure

from z3c.form.object import registerFactoryAdapter
from zope.schema import ASCIILine
from zope.schema import Date
from zope.schema import Dict
from zope.schema import List
from zope.schema import Object
from zope.schema import Text
from zope.schema.fieldproperty import FieldProperty


@provider(IFormFieldProvider)
class IScheduledContent(Interface):

    fieldset(
        "schedule",
        label=_("Schedule"),
        fields=["schedule"],
    )

    schedule = Schedule(
        title=_("Schedule"),
        key_type=ASCIILine(),
        value_type=Dict(key_type=ASCIILine(), value_type=ASCIILine()),
        required=False,
    )


@implementer(IScheduledContent)
@adapter(IDexterityContent)
class ScheduledContent(object):
    def __init__(self, context):
        self.context = context


class WidgetView(WidgetsView):
    schema = IScheduledContent


class IDateRange(Interface):
    """IDateRange"""

    start_date = Date(
        title=_("Start date"),
    )

    end_date = Date(
        title=_("End date"),
    )


@implementer(IDateRange)
class DateRange(object):
    """DateRange"""

    start_date = FieldProperty(IDateRange["start_date"])
    end_date = FieldProperty(IDateRange["end_date"])


registerFactoryAdapter(IDateRange, DateRange)


class IScheduledWithTitle(Interface):
    """IScheduledWithTitle"""

    title = Text(
        title=_("Title"),
    )

    dates = List(
        title=_("Dates"),
        value_type=Object(__name__="DateRange", schema=IDateRange),
    )

    schedule = Schedule(
        key_type=ASCIILine(),
        value_type=Dict(key_type=ASCIILine(), value_type=ASCIILine()),
        title=_("Schedule"),
    )


@implementer(IScheduledWithTitle)
class ScheduledWithTitle(object):
    """ScheduledWithTitle"""

    title = FieldProperty(IScheduledWithTitle["title"])
    dates = FieldProperty(IScheduledWithTitle["dates"])
    schedule = FieldProperty(IScheduledWithTitle["schedule"])


registerFactoryAdapter(IScheduledWithTitle, ScheduledWithTitle)


class IMultiScheduleField(Interface):
    """Marker interface for multi schedule field"""


@implementer(IMultiScheduleField)
class MultiScheduleField(List):
    """ """


@provider(IFormFieldProvider)
class IMultiScheduledContent(Interface):

    fieldset(
        "multischedule",
        label=_("Multi Schedule"),
        fields=["schedule", "multi_schedule"],
    )

    schedule = Schedule(
        title=_("Schedule"),
        key_type=ASCIILine(),
        value_type=Dict(key_type=ASCIILine(), value_type=ASCIILine()),
        required=False,
    )

    multi_schedule = MultiScheduleField(
        title=_("Multi Schedule"),
        value_type=ScheduleWithTitle(
            __name__="MultiSchedule", schema=IScheduledWithTitle, required=False
        ),
        required=False,
    )


@implementer(IMultiScheduledContent)
@adapter(IDexterityContent)
class MultiScheduledContent(ScheduledContent):
    pass


class IExceptionalClosure(Interface):
    """IExceptionalClosure"""

    title = Text(
        title=_("Title"),
    )

    date = Date(
        title=_("Date"),
    )


@implementer(IExceptionalClosure)
class ExceptionalClosureObject(object):
    """ExceptionalClosureObject"""

    title = FieldProperty(IExceptionalClosure["title"])
    date = FieldProperty(IExceptionalClosure["date"])


registerFactoryAdapter(IExceptionalClosure, ExceptionalClosureObject)


class IExceptionalClosureField(Interface):
    """Marker interface for exceptional closure field"""


@implementer(IExceptionalClosureField)
class ExceptionalClosureField(List):
    """ """


@provider(IFormFieldProvider)
class IExceptionalClosureContent(Interface):

    fieldset(
        "exceptionalclosure",
        label=_("Exceptional closure"),
        fields=["exceptional_closure"],
    )

    exceptional_closure = ExceptionalClosureField(
        title=_("Dates"),
        value_type=ExceptionalClosure(
            __name__="ExceptionalClosure", schema=IExceptionalClosure, required=False
        ),
        required=False,
    )


@implementer(IExceptionalClosureContent)
@adapter(IDexterityContent)
class ExceptionalClosureContent(object):
    def __init__(self, context):
        self.context = context
