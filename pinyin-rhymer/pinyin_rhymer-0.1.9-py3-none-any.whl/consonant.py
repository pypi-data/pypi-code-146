from enum import Enum, auto

from pinyin_rhymer.error import NotAConsonantError


class ConsonantFamily(Enum):
    Plosives = auto()
    Affricates = auto()
    Fricatives = auto()
    Laterals = auto()
    Nasals = auto()
    Others = auto()

    def __str__(self):
        return self.name

    @classmethod
    def _missing_(cls, name):
        return cls[name]


class Consonant(Enum):
    b = 'Plosives'
    d = 'Plosives'
    g = 'Plosives'
    p = 'Plosives'
    t = 'Plosives'
    k = 'Plosives'
    z = 'Affricates'
    zh = 'Affricates'
    j = 'Affricates'
    c = 'Affricates'
    ch = 'Affricates'
    q = 'Affricates'
    f = 'Fricatives'
    x = 'Fricatives'
    s = 'Fricatives'
    sh = 'Fricatives'
    h = 'Fricatives'
    l = 'Laterals'
    r = 'Laterals'
    m = 'Nasals'
    n = 'Nasals'
    Empty = 'Others'

    def __new__(cls, family):
        count = len(cls.__members__)
        obj = object.__new__(cls)
        obj._value_ = count
        obj.family = ConsonantFamily(family)
        return obj

    def __repr__(self):
        return f'{self.__class__.__name__}.{self.name}'

    def __hash__(self):
        return hash((self.family, self.name))

    def __str__(self):
        return '' if self.name == 'Empty' else self.name

    def __eq__(self, other):
        return str(self) == str(other)

    @classmethod
    def _missing_(cls, name):
        if isinstance(name, cls):
            return name
        if not name:
            return Consonant.Empty
        try:
            return getattr(cls, name)
        except AttributeError:
            pass

        try:
            translated = (
                name.replace('Z', 'zh').replace('C', 'ch').replace('S', 'sh')
            )
            return cls[translated]
        except KeyError:
            raise NotAConsonantError(name)

    @classmethod
    def all(cls):
        return set(cls)

    @classmethod
    def all_as_str(cls):
        return set(map(str, cls))

    def all_family(self):
        return {
            x for x in self.__class__ if x.family == self.family
        }
