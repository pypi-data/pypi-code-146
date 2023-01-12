# encoding: utf-8
from collective.schedulefield.behavior import IMultiScheduledContent
from collective.schedulefield.behavior import IExceptionalClosureContent
from datetime import date as dt


def get_schedule_by_date(context, date):
    """get_schedule_by_date

    :param context: IMultiScheduledContent
    :param date: Date
    """
    if IMultiScheduledContent.providedBy(context):
        multi_schedule = getattr(context, "multi_schedule", None) or []
        for i in multi_schedule:
            schedule = i.schedule
            dates = i.dates or []
            for d in dates:
                if d.start_date <= date <= d.end_date:
                    return schedule
        return getattr(context, "schedule", None)


def get_exceptionalclosure_by_date(context, date):
    """get_exceptionalclosure_by_date

    :param context:
    :param date:
    """
    if IExceptionalClosureContent.providedBy(context):
        dates = getattr(context, "exceptional_closure", None) or []
        for d in dates:
            if dt.today() == d.date:
                return d
