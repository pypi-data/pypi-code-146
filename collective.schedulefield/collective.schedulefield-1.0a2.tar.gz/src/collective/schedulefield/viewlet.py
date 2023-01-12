# -*- coding: utf-8 -*-
"""
collective.schedulefield
------------------------

Created by mpeeters
:license: GPL, see LICENCE.txt for more details.
"""

from collective.schedulefield.behavior import IExceptionalClosureContent
from collective.schedulefield.behavior import IMultiScheduledContent
from collective.schedulefield.behavior import IScheduledContent
from datetime import date
from datetime import timedelta
from plone.app.layout.viewlets import common as base
from plone.autoform.view import WidgetsView


TIMEDELTA = 14


class ScheduledContentViewlet(WidgetsView, base.ViewletBase):
    schema = IScheduledContent

    def update(self):
        if self.can_view is True:
            super(ScheduledContentViewlet, self).update()

    @property
    def has_value(self):
        schedule = getattr(self.context, "schedule", None)
        if schedule:
            for day in schedule.values():
                if len([v for v in day.values() if v]) > 0:
                    return True
        return False

    @property
    def can_view(self):
        return IScheduledContent.providedBy(self.context)


class MultiScheduledContentViewlet(ScheduledContentViewlet):
    schema = IMultiScheduledContent

    @property
    def has_closure(self):
        dates = getattr(self.context, "exceptional_closure", None) or []
        if date.today() in [d.date for d in dates]:
            return True
        return False

    @property
    def has_value(self):
        if self.has_closure:
            return False
        multi_schedule = getattr(self.context, "multi_schedule", None) or []
        for i in multi_schedule:
            dates = i.dates or []
            for d in dates:
                if d.start_date <= date.today() <= d.end_date:
                    return False
        return super(MultiScheduledContentViewlet, self).has_value

    @property
    def get_multischedule(self):
        if self.has_closure:
            return []
        widgets = []
        multi_schedule = self.w.get("multi_schedule").widgets
        for i in multi_schedule:
            schedule = i._value["schedule"]
            if schedule:
                for day in schedule.values():
                    if len([v for v in day.values() if v]) > 0:
                        dates = i._value["dates"] or []
                        for d in dates:
                            if (
                                d.start_date - timedelta(days=TIMEDELTA)
                                <= date.today()
                                <= d.end_date
                            ):
                                widgets.append(i)
        return widgets

    @property
    def can_view(self):
        return IMultiScheduledContent.providedBy(self.context)


class ExceptionalClosureContentViewlet(WidgetsView, base.ViewletBase):
    schema = IExceptionalClosureContent

    def update(self):
        if self.can_view is True:
            super(ExceptionalClosureContentViewlet, self).update()

    @property
    def get_closure(self):
        dates = self.w.get("exceptional_closure").widgets
        for d in dates:
            if date.today() == d._value["date"]:
                return d

    @property
    def can_view(self):
        return IExceptionalClosureContent.providedBy(self.context)
