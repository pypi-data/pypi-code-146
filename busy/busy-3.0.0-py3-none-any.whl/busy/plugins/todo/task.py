import re

from ...item import Item
from busy import dateparser

MARKER = re.compile(r'\s*\-*\>\s*')
REPEAT = re.compile(r'^\s*repeat(?:\s+[io]n)?\s+(.+)\s*$', re.I)
RESOURCE = re.compile(r'\s+at\s+(\S+)')

class Task(Item):

    def __init__(self, description=None):
        super().__init__(description)

    def as_plan(self, date):
        return Plan(self.description, date)

    def as_done(self, date):
        return DoneTask(self._marker_split[0], date)

    def as_followon(self):
        if len(self._marker_split) > 1:
            description = self._marker_split[1]
            if not REPEAT.match(description):
                return Task(description)

    def as_repeat(self):
        if len(self._marker_split) > 1:
            match = REPEAT.match(self._marker_split[1])
            if match:
                date = dateparser.relative_date(match.group(1))
                return Plan(self.description, date)

    @property
    def project(self):
        tags = self.tags
        return tags[0] if tags else None

    @property
    def _marker_split(self):
        return MARKER.split(self.description, maxsplit=1)

    @property
    def resource(self):
        match = RESOURCE.search(self.description)
        if match:
            return match.group(1)
        else:
            return ""

    @property
    def without_resource(self):
        split = RESOURCE.split(self.description, maxsplit=1)
        if len(split) > 1:
            return split[0] + split[2]
        else:
            return self.description


class Plan(Item):

    schema = ['date', 'description']
    listfmt = "{1.date:%Y-%m-%d}  {1.description}"

    def __init__(self, description=None, date=None):
        super().__init__(description)
        self._date = dateparser.absolute_date(date)

    @property
    def date(self):
        return self._date

    def as_todo(self):
        return Task(self.description)


class DoneTask(Item):

    schema = ['date', 'description']
    listfmt = "{1.date:%Y-%m-%d}  {1.description}"

    def __init__(self, description=None, date=None):
        super().__init__(description)
        self._date = dateparser.absolute_date(date)

    @property
    def date(self):
        return self._date
