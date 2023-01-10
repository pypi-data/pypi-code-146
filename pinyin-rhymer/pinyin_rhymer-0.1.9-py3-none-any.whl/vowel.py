import math
from enum import Enum

from pinyin_rhymer.error import NotAVowelError
from pinyin_rhymer.rhyme_scheme import VowelScheme

VOWEL_TRANSLATION = {
    'i': 'yi',
    'ie': 'ye',
    'ia': 'ya',
    'iu': 'you',
    'iao': 'yao',
    'in': 'yin',
    'ian': 'yan',
    'ing': 'ying',
    'iong': 'yong',
    'iang': 'yang',
    'u': 'wu',
    'o': 'wo',
    'uo': 'wo',
    'ua': 'wa',
    'ui': 'wei',
    'uai': 'wai',
    'uan': 'wan',
    'un': 'wen',
    'uang': 'wang',
    'ue': 'yue',
    'yv': 'yu',
    'v': 'yu',
    'yve': 'yue',
    've': 'yue',
    'yvn': 'yun',
    'vn': 'yun',
    'yvan': 'yuan',
    'van': 'yuan'
}


def _chk_same_family(this, other, family):
    return all(x in family for x in (this, other))


def _chk_add_sub(this, other):
    return (
        this.medial in other.medial and
        len(other.medial) - len(this.medial) == 1 and
        other.coda == this.coda
    ) or (
        this.coda in other.coda and
        len(other.coda) - len(this.coda) == 1 and
        other.medial == this.medial
    )


class Monophthong(Enum):
    n = (-0.1, 0.5)
    ng = (0.2, 1)
    z = (0, 0.3)
    v = (0.12, 0.18)
    u = (0.1, 0.9)
    i = (0.2, 0.1)
    r = (0.22, 0.7)
    ɚ = (0.4, 0.9)
    e = (0.4, 0.5)
    ə = (0.5, 0.55)
    ɤ = (0.5, 0.8)
    o = (0.7, 0.9)
    a = (0.95, 0.64)

    def __init__(self, openness, backness):
        self.openness = openness
        self.backness = backness

    @classmethod
    def _missing_(cls, name):
        return cls[name]

    def similar(self, threshold):
        return Monophthong.similar_to(self.value, threshold)

    @classmethod
    def similar_to(cls, value, threshold):
        return {
            m for m in Monophthong if (
                math.hypot(
                    *[v for v in [abs(a - b) for (a, b) in zip(m.value, value)]]
                ) < threshold
            )
        }


class Multiphthong(object):
    @staticmethod
    def _weighted_average(values, weights):
        return sum(v * d for (v, d) in zip(values, weights)) / sum(weights)

    @classmethod
    def altered_nucleus(cls, vowel, ratios=(8, 1)):
        body = Monophthong(vowel.nucleus)
        if not vowel.coda:
            return body.value
        tail = Monophthong(vowel.coda)

        openness = cls._weighted_average(
            list(x.openness for x in (body, tail)), ratios
        )
        backness = cls._weighted_average(
            list(x.backness for x in (body, tail)), ratios
        )
        return (openness, backness)

    @classmethod
    def compare_average(cls, this, other, threshold=0.15):
        return all(
            abs(x - y) < threshold for (x, y) in zip(this, other)
        )


class MouthMovement(Enum):
    NO_MOVEMENT = (0, 0)
    FRONT = (0, -1)
    BACK = (0, 1)
    CLOSE = (-1, 0)
    OPEN = (1, 0)
    CLOSE_FRONT = (-1, -1)
    CLOSE_BACK = (-1, 1)
    OPEN_FRONT = (1, -1)
    OPEN_BACK = (1, 1)

    @staticmethod
    def cmp(a, b, threshold):
        return ((a - b) > threshold) - ((b - a) > threshold)

    @classmethod
    def get_movement(cls, source, target, threshold=0.15):
        openness = cls.cmp(target.openness, source.openness, threshold)
        backness = cls.cmp(target.backness, source.backness, threshold)
        return MouthMovement((openness, backness))

    @classmethod
    def calculate(cls, vowel, threshold):
        if vowel == Vowel.Empty:
            return (None, None)
        try:
            source = Monophthong(vowel.nucleus)
        except KeyError:
            return MouthMovement.NO_MOVEMENT

        try:
            target = Monophthong(vowel.coda)
        except KeyError:
            if not vowel.medial:
                return MouthMovement.NO_MOVEMENT
            target = source
            source = Monophthong(vowel.medial)

        return cls.get_movement(source, target, threshold)


class Vowel(Enum):
    e = ('e', '', 'ɤ', '')
    a = ('a', '', 'a', '')
    ei = ('ei', '', 'e', 'i')
    ai = ('ai', '', 'a', 'i')
    o = ('o', '', 'o', '')
    ou = ('ou', '', 'o', 'u')
    ao = ('ao', '', 'a', 'u')
    en = ('en', '', 'ə', 'n')
    an = ('an', '', 'a', 'n')
    eng = ('eng', '', 'ə', 'ng')
    ang = ('ang', '', 'a', 'ng')
    ong = ('ong', '', 'o', 'ng')
    er = ('er', '', 'ɚ', '')
    yi = ('i', '', 'i', '')
    z = ('i', '', 'z', '')
    r = ('i', '', 'r', '')
    ye = ('ie', 'i', 'e', '')
    ya = ('ia', 'i', 'a', '')
    you = ('iu', 'i', 'o', 'u')
    yao = ('iao', 'i', 'a', 'u')
    yo = ('io', 'i', 'o', '')
    yin = ('in', '', 'i', 'n')
    yan = ('ian', 'i', 'a', 'n')
    ying = ('ing', '', 'i', 'ng')
    yong = ('iong', 'i', 'o', 'ng')
    yang = ('iang', 'i', 'a', 'ng')
    wu = ('u', '', 'u', '')
    wo = ('uo', 'u', 'o', '')
    wa = ('ua', 'u', 'a', '')
    wei = ('ui', 'u', 'e', 'i')
    wai = ('uai', 'u', 'a', 'i')
    wen = ('un', 'u', 'ə', 'n')
    wan = ('uan', 'u', 'a', 'n')
    weng = ('weng', 'u', 'ə', 'ng')
    wang = ('uang', 'u', 'a', 'ng')
    yu = ('v', '', 'v', '')
    yue = ('ue', 'v', 'e', '')
    yun = ('vn', '', 'v', 'n')
    yuan = ('van', 'v', 'a', 'n')
    Empty = ('', '', '', '')

    def __new__(cls, spell, medial, nucleus, coda):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        obj.spell = spell
        obj.medial = medial
        obj.nucleus = nucleus
        obj.coda = coda
        return obj

    def __repr__(self):
        return f'{self.__class__.__name__}.{self.name}'

    @classmethod
    def _missing_(cls, s):
        if not s:
            return Vowel.Empty
        if s in VOWEL_TRANSLATION:
            s = VOWEL_TRANSLATION[s]
        try:
            return Vowel[s]
        except KeyError:
            raise NotAVowelError(s)

    @property
    def with_consonant(self):
        return self.spell

    @property
    def without_consonant(self):
        return (
            'yi' if self.spell == 'i' else
            '' if self == Vowel.Empty else
            self.name
        )

    def rhyme(self, rhymescheme, *args, **kwargs):
        if self == Vowel.Empty:
            return {}
        if not isinstance(rhymescheme, VowelScheme):
            rhymescheme = VowelScheme(rhymescheme)
        match rhymescheme:
            case VowelScheme.FOURTEEN_RHYMES:
                return self._fourteen_rhymes(*args, **kwargs)
            case VowelScheme.SIMILAR_BODY:
                return self._similar_nucleus(*args, **kwargs)
            case VowelScheme.SIMILAR_TAIL:
                return self._similar_coda(*args, **kwargs)
            case VowelScheme.SIMILAR_SOUNDING:
                return self._similar_sounding(*args, **kwargs)
            case VowelScheme.SIMILAR_MULTIPHTHONG:
                return self._similar_multiphthong(*args, **kwargs)
            case VowelScheme.SIMILAR_MOUTH_MOVEMENT:
                return self._similar_mouth_movement(*args, **kwargs)
            case VowelScheme.ADDITIVE:
                return self._additive_rhymes(*args, **kwargs)
            case VowelScheme.SUBTRACTIVE:
                return self._subtractive_rhymes(*args, **kwargs)

    def _fourteen_rhymes(self, *args, **kwargs):
        cls = self.__class__
        return {x for x in cls if x.coda == self.coda and (
            not x.coda and (
                _chk_same_family(self, x, (Vowel.z, Vowel.r)) or
                _chk_same_family(self, x, (
                    Vowel.e, Vowel.o, Vowel.yo, Vowel.wo
                    )) or
                _chk_same_family(self, x, (Vowel.yi, Vowel.yu, Vowel.er))
            ) or (
                x.nucleus == self.nucleus or (
                    'n' in x.coda and
                    _chk_same_family(self.nucleus, x.nucleus, 'əiuov')
                )
            )
        )}

    def _similar_nucleus(self, *args, **kwargs):
        threshold = 0.1 + kwargs.get('more', 0) * 0.1
        body = Multiphthong.altered_nucleus(self)
        similar = Monophthong.similar_to(body, threshold=threshold)
        return {
            x for x in Vowel if x is not Vowel.Empty and any(
                Multiphthong.compare_average(
                    Multiphthong.altered_nucleus(x),
                    y.value,
                    threshold=threshold
                ) for y in similar
            )
        }

    def _similar_coda(self, *args, **kwargs):
        threshold = 0.1 + kwargs.get('more', 0) * 0.1
        tail = Monophthong(self.coda or self.nucleus)
        similar = {x.name for x in tail.similar(threshold=threshold)}
        return {
            x for x in Vowel if (
                x.coda in similar if x.coda else x.nucleus in similar
            )
        }

    def _similar_sounding(self, *args, **kwargs):
        more = kwargs.pop('more', 0) * 0.75
        body_rhymes = self._similar_nucleus(*args, more=more+0.25, **kwargs)
        tail_rhymes = self._similar_coda(*args, more=more+0.25, **kwargs)
        return body_rhymes.intersection(tail_rhymes)

    def _similar_mouth_movement(self, *args, **kwargs):
        threshold = 0.15 + kwargs.get('more', 0) * 0.15
        self_movement = MouthMovement.calculate(self, threshold=threshold)
        return {
            x for x in Vowel if
            MouthMovement.calculate(x, threshold=threshold) == self_movement
        }

    def _additive_rhymes(self, *args, **kwargs):
        cls = self.__class__
        return {x for x in cls if x is not Vowel.Empty and (
            x == self or
            (
                x.nucleus == self.nucleus and _chk_add_sub(self, x)
            ) or (
                x.medial == self.nucleus and not x.coda
            )
        )}

    def _subtractive_rhymes(self, *args, **kwargs):
        cls = self.__class__
        return {x for x in cls if x is not Vowel.Empty and (
            x == self or
            (
                x.nucleus == self.nucleus and _chk_add_sub(x, self)
            ) or (
                not self.coda and
                self.medial == x.nucleus and
                not x.medial and not x.coda
            )
        )}
