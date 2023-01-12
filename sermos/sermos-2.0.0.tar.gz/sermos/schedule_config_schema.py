""" Schemas for Schedule Configuration
"""
import re
from croniter import croniter
from marshmallow.validate import OneOf
from marshmallow.exceptions import ValidationError
from marshmallow import Schema, fields, EXCLUDE, pre_load, validates_schema


class ExcludeUnknownSchema(Schema):
    """ Remove unknown keys from loaded dictionary

    # TODO this seems to be just ignoring and letting through vs excluding...
    """
    class Meta:
        unknown = EXCLUDE


class IntervalScheduleSchema(Schema):
    every = fields.Integer(required=True)
    period = fields.String(
        required=True,
        validate=OneOf(['microseconds', 'seconds', 'minutes', 'hours',
                        'days']))


class CrontabScheduleSchema(Schema):
    minute = fields.String(required=True)
    hour = fields.String(required=True)
    dayOfWeek = fields.String(required=True)
    dayOfMonth = fields.String(required=True)
    monthOfYear = fields.String(required=True)

    @validates_schema
    def validate_values(self, data, **kwargs):
        if data['minute'] is None or data['hour'] is None or \
            data['dayOfWeek'] is None or data['dayOfMonth'] is None or\
                data['monthOfYear'] is None:
            raise ValidationError("Empty crontab value")

        test_cron_expression = \
            f"{data['minute']} {data['hour']} {data['dayOfMonth']} " \
            f"{data['monthOfYear']} {data['dayOfWeek']}"

        if not croniter.is_valid(test_cron_expression):
            return ValidationError("Invalid crontab value")


class Schedule(fields.Dict):
    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        if data['scheduleType'] == 'crontab':
            schema = CrontabScheduleSchema()
        else:
            schema = IntervalScheduleSchema()
        return schema.load(value)


class ScheduleConfigSchemaV1(ExcludeUnknownSchema):
    """ Definition of a single schedule entry

    TODO: Add validation based on schedule_type and the relevant optional fields
    TODO: Add validation that each name is unique
    """

    scheduleType = fields.String(
        required=True,
        validate=OneOf(['interval', 'crontab']),
        description="The Celery schedule type of this entry.",
        example="interval",
        data_key='scheduleType')

    queue = fields.String(required=True,
                          description="Name of queue on which to place task.",
                          example="my-default-queue")
    task = fields.String(required=True,
                         description="Path to task to invoke.",
                         example="my_app.module.method")
    exchange = fields.String(
        required=False,
        description="Exchange for the task. Celery default "
        "used if not set, which is recommended.",
        example="tasks")
    routing_key = fields.String(
        required=False,
        description="Routing key for the task. Celery "
        "default used if not set, which is recommended.",
        example="task.default",
        data_key='routingKey')
    expires = fields.Integer(
        required=False,
        description="Number of seconds after which task "
        "expires if not executed. Default: no expiration.",
        example=60)

    schedule = Schedule(required=True)

    @pre_load
    def validate_string_fields(self, item, **kwargs):
        """ Ensure string fields with no OneOf validation conform to patterns
        """
        if item is None:
            raise ValidationError("NoneType provided, check input.")

        validation_map = {
            'name': r'^[\w\d\-\_\.\s]+$',
            'queue': r'^[\w\d\-\_\.]+$',
            'task': r'^[\w\d\-\_\.]+$',
            'exchange': r'^[\w\d\-\_\.]+$',
            'routing_key': r'^[\w\d\-\_\.]+$'
        }
        for field in validation_map:
            if item.get(field, None) is None:
                continue
            if not bool(re.match(validation_map[field], item[field])):
                raise ValidationError(
                    f"Invalid {field}: `{item[field]}``. Must match pattern: "
                    f"{validation_map[field]}")

        if 'scheduleType' not in item:
            raise ValidationError('Missing required field scheduleType')

        if item['scheduleType'] == 'crontab':
            cron_validation_map = {
                'minute': crontab_parser(60),
                'hour': crontab_parser(24),
                'dayOfWeek': crontab_parser(7),
                'dayOfMonth': crontab_parser(31, 1),
                'monthOfYear': crontab_parser(12, 1)
            }

            for field in cron_validation_map:
                try:
                    cron_validation_map[field].parse(item['schedule'][field])
                except:
                    raise ValidationError(
                        f"Invalid {field}: `{item['schedule'][field]}`. Must "
                        "be valid crontab pattern.")

        return item


class BaseScheduleSchema(ExcludeUnknownSchema):
    __schema_version__ = 0

    name = fields.String(required=True,
                         description="Name of schedule entry.",
                         example="My Scheduled Task")
    schemaVersion = fields.Integer(required=True)
    config = fields.Dict(required=True)
    enabled = fields.Boolean(required=True,
                             description="Whether entry is enabled.",
                             example=True)
    # TODO Figure out where that wonky timestamp format is coming from and
    # update this and in celery_beat.py.
    lastRunAt = fields.DateTime(allow_none=True,
                                missing=None,
                                description="Timestamp of last run time.",
                                example="Tue, 18 Aug 2020 01:36:06 GMT",
                                data_key='lastRunAt')
    totalRunCount = fields.Integer(
        allow_none=True,
        missing=0,
        description="Count of number of executions.",
        example=12345,
        data_key='totalRunCount')

    @classmethod
    def get_by_version(cls, version):
        for subclass in cls.__subclasses__():
            if subclass.__schema_version__ == version:
                return subclass

        return None

    @classmethod
    def get_latest(cls):
        max_version = 0
        max_class = None
        for subclass in cls.__subclasses__():
            if subclass.__schema_version__ > max_version:
                max_version = max_version
                max_class = subclass

        return max_class

    @validates_schema
    def validate_scheduled_tasks(self, data, **kwargs):
        schema_version = data['schemaVersion']
        TaskSchema = BaseScheduleSchema.get_by_version(schema_version)
        schema = TaskSchema()
        schema.load(data)


class ScheduleSchemaV1(BaseScheduleSchema):
    __schema_version__ = 1

    config = fields.Nested(
        ScheduleConfigSchemaV1,
        required=True,
        description="Configuration information for this schedule.")

    def validate_scheduled_tasks(self, data, **kwargs):
        # We need to add this function to avoid infinite recursion since
        # the BaseScheduleSchema class above uses the same method for
        # validation
        pass


class ParseException(Exception):
    """Raised by :class:`crontab_parser` when the input can't be parsed."""


class crontab_parser:
    """ Parser for Crontab expressions.

        Copied from
        https://github.com/celery/celery/blob/main/celery/schedules.py
        in order to remove the dependency on Celery for this single class.

        Copyright (c) 2015-2016 Ask Solem & contributors.  All rights reserved.
        Copyright (c) 2012-2014 GoPivotal, Inc.  All rights reserved.
        Copyright (c) 2009, 2010, 2011, 2012 Ask Solem, and individual contributors.  All rights reserved.

        Any expression of the form 'groups'
        (see BNF grammar below) is accepted and expanded to a set of numbers.
        These numbers represent the units of time that the Crontab needs to
        run on:
        .. code-block:: bnf
            digit   :: '0'..'9'
            dow     :: 'a'..'z'
            number  :: digit+ | dow+
            steps   :: number
            range   :: number ( '-' number ) ?
            numspec :: '*' | range
            expr    :: numspec ( '/' steps ) ?
            groups  :: expr ( ',' expr ) *
        The parser is a general purpose one, useful for parsing hours, minutes and
        day of week expressions.  Example usage:
        .. code-block:: pycon
            >>> minutes = crontab_parser(60).parse('*/15')
            [0, 15, 30, 45]
            >>> hours = crontab_parser(24).parse('*/4')
            [0, 4, 8, 12, 16, 20]
            >>> day_of_week = crontab_parser(7).parse('*')
            [0, 1, 2, 3, 4, 5, 6]
        It can also parse day of month and month of year expressions if initialized
        with a minimum of 1.  Example usage:
        .. code-block:: pycon
            >>> days_of_month = crontab_parser(31, 1).parse('*/3')
            [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31]
            >>> months_of_year = crontab_parser(12, 1).parse('*/2')
            [1, 3, 5, 7, 9, 11]
            >>> months_of_year = crontab_parser(12, 1).parse('2-12/2')
            [2, 4, 6, 8, 10, 12]
        The maximum possible expanded value returned is found by the formula:
            :math:`max_ + min_ - 1`
    """

    ParseException = ParseException

    _range = r'(\w+?)-(\w+)'
    _steps = r'/(\w+)?'
    _star = r'\*'

    def __init__(self, max_=60, min_=0):
        self.max_ = max_
        self.min_ = min_
        self.pats = (
            (re.compile(self._range + self._steps), self._range_steps),
            (re.compile(self._range), self._expand_range),
            (re.compile(self._star + self._steps), self._star_steps),
            (re.compile('^' + self._star + '$'), self._expand_star),
        )

    def parse(self, spec):
        acc = set()
        for part in spec.split(','):
            if not part:
                raise self.ParseException('empty part')
            acc |= set(self._parse_part(part))
        return acc

    def _parse_part(self, part):
        for regex, handler in self.pats:
            m = regex.match(part)
            if m:
                return handler(m.groups())
        return self._expand_range((part, ))

    def _expand_range(self, toks):
        fr = self._expand_number(toks[0])
        if len(toks) > 1:
            to = self._expand_number(toks[1])
            if to < fr:  # Wrap around max_ if necessary
                return (list(range(fr, self.min_ + self.max_)) +
                        list(range(self.min_, to + 1)))
            return list(range(fr, to + 1))
        return [fr]

    def _range_steps(self, toks):
        if len(toks) != 3 or not toks[2]:
            raise self.ParseException('empty filter')
        return self._expand_range(toks[:2])[::int(toks[2])]

    def _star_steps(self, toks):
        if not toks or not toks[0]:
            raise self.ParseException('empty filter')
        return self._expand_star()[::int(toks[0])]

    def _expand_star(self, *args):
        return list(range(self.min_, self.max_ + self.min_))

    def _expand_number(self, s):
        if isinstance(s, str) and s[0] == '-':
            raise self.ParseException('negative numbers not supported')
        try:
            i = int(s)
        except ValueError:
            try:
                i = weekday(s)
            except KeyError:
                raise ValueError(f'Invalid weekday literal {s!r}.')

        max_val = self.min_ + self.max_ - 1
        if i > max_val:
            raise ValueError(f'Invalid end range: {i} > {max_val}.')
        if i < self.min_:
            raise ValueError(f'Invalid beginning range: {i} < {self.min_}.')

        return i
