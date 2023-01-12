# -*- coding: utf-8 -*-

import json
from datetime import time

from zope import schema
from zope.component import adapter
from zope.component import adapts
from zope.interface import implementer
from zope.schema.interfaces import IDict
from zope.schema.interfaces import IObject
from zope.schema.interfaces import IFromUnicode
from zope.schema.interfaces import WrongContainedType

from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import NO_VALUE
from z3c.form.object import ObjectWidget

from z3c.form.converter import BaseDataConverter
from z3c.form.widget import FieldWidget
from z3c.form.widget import Widget
from z3c.form.browser.widget import HTMLInputWidget
from z3c.form.browser.widget import HTMLFormElement

from collective.schedulefield import _


class ISchedule(IDict):
    """ """


class IScheduleWithTitle(IObject):
    """IScheduleWithTitle"""


@implementer(IScheduleWithTitle)
class ScheduleWithTitle(schema.Object):
    """ """


@implementer(ISchedule, IFromUnicode)
class Schedule(schema.Dict):
    def fromUnicode(self, value):
        """ """
        self.validate(value)
        return value

    def validate(self, value):
        if value is None or value is NO_VALUE:
            return
        if type(value) != dict:
            value = json.loads(value)
        for day in value:
            for section in value[day]:
                if section == "comment":
                    continue
                error = self._validate_format(value[day][section])
                if error:
                    raise WrongContainedType(error, self.__name__)

    def _validate_format(self, data):
        """
        12:10 > time(12, 10)
        """
        if not data:
            return None
        hour, minute = data.split(":")
        try:
            time(int(hour), int(minute))
        except ValueError:
            return _("Not a valid time format.")

        return None


@implementer(ISchedule)
class ScheduleWidget(HTMLInputWidget, Widget):

    """Schedule widget implementation."""

    klass = "schedule-widget"
    css = "schedule"
    value = ""
    size = None
    maxlength = None

    @property
    def days(self):
        return (
            ("monday", _("Monday")),
            ("tuesday", _("Tuesday")),
            ("wednesday", _("Wednesday")),
            ("thursday", _("Thursday")),
            ("friday", _("Friday")),
            ("saturday", _("Saturday")),
            ("sunday", _("Sunday")),
        )

    @property
    def day_sections(self):
        return ("morningstart", "morningend", "afternoonstart", "afternoonend")

    def update(self):
        super(ScheduleWidget, self).update()
        if self.value and self.value is not NO_VALUE and type(self.value) != dict:
            self.value = json.loads(self.value)

    def extract(self):
        datas = {}
        is_empty = True
        for key, name in self.days:
            datas[key] = {
                "comment": self.request.get(
                    "{0}.{1}.comment".format(self.name, key),
                ),
            }
            for day_section in self.day_sections:
                data = self.request.get(
                    "{0}.{1}.{2}".format(self.name, key, day_section),
                    None,
                )
                formated = self._format(data)
                datas[key][day_section] = formated
                if formated is not None:
                    is_empty = False

        if is_empty:
            return NO_VALUE
        return json.dumps(datas)

    def get_hour_value(self, day, day_section):
        """
        return hour for a specific day section
        """
        if (not self.value) or (self.value is NO_VALUE):
            return ""
        return self.value.get(day).get(day_section)

    def get_comment(self, day):
        """Return the comment for a specific day"""
        if not self.value or self.value is NO_VALUE:
            return ""
        return self.value.get(day).get("comment")

    @staticmethod
    def _format(data):
        if data == "__:__":
            return None
        return data

    def must_show_day(self, day):
        """
        Tell if template must show the day or not
        We do not show days without value
        """
        must_show = False
        if not self.value:
            return must_show
        for day_section in self.day_sections:
            if self.value.get(day).get(day_section) or self.value.get(day).get(
                "comment"
            ):
                must_show = True
        return must_show


@implementer(IScheduleWithTitle)
class ScheduleWithTitleWidget(HTMLFormElement, ObjectWidget):

    klass = "object-widget"
    css = "object"


class WidgetDataConverter(BaseDataConverter):
    adapts(ISchedule, IFieldWidget)

    def toWidgetValue(self, value):
        if value is not None and type(value) != dict:
            return json.loads(value)
        return value

    def toFieldValue(self, value):
        if value is not None and type(value) != dict:
            return json.loads(value)
        return value


@adapter(ISchedule, IFormLayer)
@implementer(IFieldWidget)
def ScheduleFieldWidget(field, request):
    """IFieldWidget factory for cheduleWidget."""
    return FieldWidget(field, ScheduleWidget(request))


@adapter(IObject, IFormLayer)
@implementer(IFieldWidget)
def ObjectFieldWidget(field, request):
    """IFieldWidget factory for IObjectWidget."""
    return FieldWidget(field, ScheduleWithTitleWidget(request))
