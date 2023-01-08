import uuid
from uuid import UUID as UUID_IMPL
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ID:
    _uuid: UUID_IMPL

    @staticmethod
    def from_string(potential_uuid_value):
        if not potential_uuid_value:
            return InvalidID()
        try:
            return ID(UUID_IMPL(potential_uuid_value))
        except ValueError as e:
            return InvalidID()

    @staticmethod
    def invalid():
        return InvalidID()

    @property
    def valid(self):
        return True

    def __str__(self):
        return str(self._uuid)


class IDGenerator(object):
    def generate_id(self):
        return ID(uuid.uuid4())


class FixedIDGeneratorGenerating(IDGenerator):
    def __init__(self, *ids):
        for id in ids:
            assert id.__class__ == ID
        self.ids = ids
        self.index = -1

    def generate_id(self):
        self.index = (self.index + 1) % len(self.ids)
        return self.ids[self.index]


class InvalidValidGenerator:
    counter = 0

    @staticmethod
    def next_invalid_value():
        print('generating')
        return 'invalid_id_{}'.format(InvalidValidGenerator.next())

    @staticmethod
    def next():
        InvalidValidGenerator.counter += 1
        return InvalidValidGenerator.counter


@dataclass(frozen=True)
class InvalidID:
    value: str = field(default_factory=InvalidValidGenerator.next_invalid_value)

    @property
    def valid(self):
        return False

    def __str__(self):
        return self.value
