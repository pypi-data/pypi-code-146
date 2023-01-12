import enum

from django.utils.functional import Promise


class Choice:

    def __init__(self, value, label=None, next=None, initial=True, **kwargs):
        self.value = value
        self.label = label
        self.next = next
        self.initial = initial
        self.extra = kwargs


def set_enum_attribute(enum, name, value_map):
    setattr(enum, name, property(lambda self: value_map[self.value].get(name)))


class ChoiceEnumMeta(enum.EnumMeta):

    def __new__(metacls, classname, bases, classdict, **kwds):
        extra_keys = {'next', 'initial'}
        extra_data = []

        # Always is expected that start will be 1
        auto_start = 1
        auto_last_values = []
        auto_count = 0

        for key in classdict._member_names:
            value = classdict[key]
            member_extra_data = {
                'next': None,
                'initial': True,
                'label': key.replace('_', ' ').title()
            }
            if isinstance(value, Choice):
                choice = value
                value = choice.value
                label = choice.label
                member_extra_data.update(
                    {
                        'next': choice.next,
                        'initial': choice.initial,
                        **choice.extra
                    }
                )

            elif (
                    isinstance(value, (list, tuple)) and
                    len(value) > 1 and
                    isinstance(value[-1], (Promise, str))
            ):
                *value, label = value
                value = tuple(value)
                if len(value) == 1:
                    value = value[0]
            else:
                label = None

            if label is None:
                label = key.replace('_', ' ').title()

            member_extra_data['label'] = label

            extra_keys.update(member_extra_data.keys())
            extra_data.append(member_extra_data)
            if isinstance(value, enum.auto):
                value = classdict['_generate_next_value_'](key, auto_start, auto_count, auto_last_values)

            auto_count += 1
            auto_last_values.append(value)

            # Use dict.__setitem__() to suppress defenses against double
            # assignment in enum's classdict.
            dict.__setitem__(classdict, key, value)
        cls = super().__new__(metacls, classname, bases, classdict, **kwds)
        cls._value2data_map_ = dict(zip(cls._value2member_map_, extra_data))
        for key in extra_keys:
            set_enum_attribute(cls, key, cls._value2data_map_)
        return enum.unique(cls)

    def __contains__(cls, member):
        if not isinstance(member, enum.Enum):
            # Allow non-enums to match against member values.
            return any(x.value == member for x in cls)
        return super().__contains__(member)

    @property
    def names(cls):
        empty = ['__empty__'] if hasattr(cls, '__empty__') else []
        return empty + [member.name for member in cls]

    @property
    def choices(cls):
        empty = [(None, cls.__empty__)] if hasattr(cls, '__empty__') else []
        return empty + [(member.value, member.label) for member in cls]

    @property
    def labels(cls):
        return [label for _, label in cls.choices]

    @property
    def values(cls):
        return [value for value, _ in cls.choices]


def class_to_str(cls):
    if cls.__class__ == type:
        return cls
    else:
        return '{}.{}'.format(cls.__module__, cls.__name__)


class ChoicesEnum(enum.Enum, metaclass=ChoiceEnumMeta):

    def deconstruct_choice(self):
        keywords = {'value': self.value}
        if self.initial is not None:
            keywords['initial'] = self.initial
        if self.next is not None:
            keywords['next'] = self.next
        return self.name, keywords

    @classmethod
    def deconstruct_cls(cls):
        name = cls.__name__
        if len(cls.__bases__) > 2:
            return name, class_to_str(cls), None, None
        if len(cls.__bases__) == 1:
            enum_type, enum_base = None, class_to_str(cls.__bases__[0])
        elif len(cls.__bases__) == 2:
            enum_type, enum_base = [class_to_str(base) for base in cls.__bases__]
        return name, enum_base, enum_type, dict(choice.deconstruct_choice() for choice in cls)

    def __str__(self):
        """
        Show our label when Django uses the Enum for displaying in a view
        """
        return str(self.label)


class IntegerChoicesEnum(int, ChoicesEnum):
    pass


class TextChoicesEnum(str, ChoicesEnum):

    def _generate_next_value_(name, start, count, last_values):
        return name
