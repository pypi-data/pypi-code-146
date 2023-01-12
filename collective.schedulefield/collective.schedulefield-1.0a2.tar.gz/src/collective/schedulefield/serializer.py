# -*- coding: utf-8 -*-

from collective.schedulefield.behavior import ExceptionalClosureObject
from collective.schedulefield.behavior import IDateRange
from collective.schedulefield.behavior import IExceptionalClosureContent
from collective.schedulefield.behavior import IExceptionalClosureField
from collective.schedulefield.behavior import IMultiScheduledContent
from collective.schedulefield.behavior import IMultiScheduleField
from collective.schedulefield.exceptionalclosure import IExceptionalClosure
from plone.restapi.deserializer.dxfields import DefaultFieldDeserializer
from plone.restapi.interfaces import IFieldDeserializer
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.interfaces import IJsonCompatible
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.dxfields import DefaultFieldSerializer
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema import getFields


@adapter(IExceptionalClosureField, IExceptionalClosureContent, Interface)
@implementer(IFieldSerializer)
class ExceptionalclosureSerializer(DefaultFieldSerializer):
    """ """

    def __call__(self):
        value = self.get_value()
        if value is None:
            return []
        closures = [json_compatible(v.__dict__) for v in value]
        return json_compatible(closures)


@implementer(IFieldDeserializer)
@adapter(IExceptionalClosure, IExceptionalClosureContent, IBrowserRequest)
class ExceptionalclosureDeserializer(DefaultFieldDeserializer):
    """ """

    def __call__(self, value):
        if "date" not in value or "title" not in value:
            raise ValueError("ExceptionalClosure dict must have title & date keys")
        closure = ExceptionalClosureObject()
        for field_name in getFields(self.field.schema):
            deserializer = getMultiAdapter(
                (self.field.schema[field_name], self.context, self.request),
                IFieldDeserializer,
            )
            setattr(closure, field_name, deserializer(value[field_name]))
        value = closure
        self.field.validate(value)
        return value


@adapter(IMultiScheduleField, IMultiScheduledContent, Interface)
@implementer(IFieldSerializer)
class MultiScheduleSerializer(DefaultFieldSerializer):
    """ """

    def __call__(self):
        value = self.get_value()
        if value is None:
            return []
        multischedules = [json_compatible(v.__dict__) for v in value]
        return json_compatible(multischedules)


@adapter(IDateRange)
@implementer(IJsonCompatible)
def daterange_converter(value):
    if value is None:
        return {}
    return {
        "start_date": json_compatible(value.start_date),
        "end_date": json_compatible(value.end_date),
    }
