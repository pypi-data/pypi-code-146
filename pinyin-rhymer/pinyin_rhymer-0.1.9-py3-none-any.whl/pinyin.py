import itertools
import re

from pinyin_rhymer.consonant import Consonant
from pinyin_rhymer.data.pinyin_list import PINYIN_LIST
from pinyin_rhymer.error import (
    NotAPinYinError, IrregularPinYinError, NotARhymeSchemeError
)
from pinyin_rhymer.rhyme_scheme import ConsonantScheme, VowelScheme
from pinyin_rhymer.vowel import Vowel

TONES = 'āēīōūǖáéíóúǘǎěǐǒǔǚàèìòùǜ'
REPLACE = 'aāáǎàeēéěèiīíǐìoōóǒòuūúǔùvǖǘǚǜ'
ZCS = ('z', 'c', 's')
ZHCHSHR = ('zh', 'ch', 'sh', 'r')
BPMF = ('b', 'p', 'm', 'f')
JQX = ('j', 'q', 'x')
IRREGULARS = ('hm', 'hng', 'ń', 'ň', 'ǹ', 'ńg', 'ňg', 'ǹg', 'ḿ', 'm̀')
_re_consonant = f'(?P<consonant>{"|".join(Consonant.all_as_str())})?'
_re_vowel = r'(?P<vowel>(?:er|[eaiouvüwy]+(?:n|ng)?))?'
_re_tone = r'(?P<tone>\d)?'
RE_PINYIN = re.compile(f'^{_re_consonant}{_re_vowel}{_re_tone}$')


def convert_unicode_to_alnum(pinyin):
    """
    Convert an unicode string of pinyin into an alphanumeric one.
    """
    for c in pinyin:
        if c in TONES:
            i = TONES.find(c)
            vowel = i % 6
            tone = i // 6 + 1
            pinyin = f'{pinyin.replace(c, REPLACE[vowel*5])}{tone}'
            break
    return pinyin.replace('ü', 'v')


def transform_vowel(consonant, vowel):
    match vowel:
        case 'i':
            if consonant in ZCS:
                return 'z'
            if consonant in ZHCHSHR:
                return 'r'
        case 'o':
            if consonant in BPMF:
                return 'uo'
    if consonant and consonant in JQX:
        if vowel != 'iu':
            return vowel.replace('u', 'v')
    return vowel.replace('yv', 'yu')


def reverse_transform_vowel(consonant, vowel):
    match vowel:
        case 'uo':
            if consonant in BPMF:
                return 'o'
    if consonant and consonant in JQX:
        return vowel.replace('v', 'u')
    return vowel


class PinYin(object):
    def __init__(self, in_str, vowel=None, tone=1):
        if isinstance(in_str, PinYin):
            self.consonant = in_str.consonant
            self.vowel = in_str.vowel
            self.tone = in_str.tone
            return
        consonant = in_str
        if not vowel:
            consonant, vowel, tone = self._parse(in_str)
        self.consonant = Consonant(consonant)
        self.vowel = Vowel(vowel)
        self.tone = int(tone)

    def _parse(self, pinyin):
        if not pinyin.isascii():
            pinyin = convert_unicode_to_alnum(pinyin)
        groups = RE_PINYIN.match(pinyin)
        if not groups:
            if pinyin in IRREGULARS:
                raise IrregularPinYinError(pinyin)
            else:
                raise NotAPinYinError(pinyin)

        consonant = groups.group('consonant')
        vowel = groups.group('vowel')
        vowel = transform_vowel(consonant, vowel)
        tone = groups.group('tone') or 5

        return consonant, vowel, tone

    def __repr__(self):
        return f'{self.__class__.__name__}("{str(self)}")'

    @property
    def spell_vowel(self):
        consonant = str(self.consonant)
        vowel = (
            self.vowel.with_consonant if consonant
            else self.vowel.without_consonant
        )
        return reverse_transform_vowel(consonant, vowel)

    @property
    def is_valid(self):
        consonant = str(self.consonant)
        match self.vowel:
            case Vowel.r:
                if consonant not in ZHCHSHR:
                    return False
            case Vowel.z:
                if consonant not in ZCS:
                    return False
            case Vowel.wu:
                if consonant in JQX:
                    return False
        return self.with_tone_mark() in PINYIN_LIST

    def __str__(self):
        return f'{self.consonant}{self.spell_vowel}{self.tone}'

    def __hash__(self):
        return hash(self.with_tone_mark())

    def __eq__(self, other):
        return str(self) == other or hash(self) == hash(other)

    def with_tone_mark(self):
        vowel = self.spell_vowel
        if self.tone == 5:
            return f'{self.consonant}{vowel}'

        if len(vowel) == 1:
            replace = vowel
        elif 'a' in vowel:
            replace = 'a'
        elif 'e' in vowel:
            replace = 'e'
        elif 'o' in vowel:
            replace = 'o'
        elif 'n' in vowel:
            replace = vowel[vowel.index('n')-1]
        else:
            replace = vowel[1]
        if self.consonant not in JQX:
            vowel = vowel.replace('ue', 'üe')
        vowel = vowel.replace(
            replace, REPLACE[REPLACE.index(replace) + (self.tone % 5)]
        )
        return f'{self.consonant}{vowel}'

    def rhymes_with(
        self,
        other,
        consonant_scheme='ALL',
        vowel_scheme=VowelScheme.SIMILAR_SOUNDING,
        tone='SAME'
    ):
        other = PinYin(other)
        rhyme_consonant = (
            other.consonant in self._get_consonant_list(consonant_scheme)
        )
        rhyme_vowel = (
            other.vowel in self._get_vowel_list(vowel_scheme)
        )
        rhyme_tone = tone != 'SAME' or other.tone == self.tone
        return rhyme_consonant and rhyme_vowel and rhyme_tone

    def generate_rhymes(
        self,
        consonants='ALL',
        vowels=VowelScheme.SIMILAR_SOUNDING,
        tones=None
    ):
        consonants = self._get_consonant_list(consonants)
        vowels = self._get_vowel_list(vowels)
        tones = tones and self._get_tone_list(tones) or (self.tone,)
        for consonant in consonants:
            for vowel in vowels:
                for tone in tones:
                    pinyin = PinYin(consonant, vowel, tone)
                    if pinyin.is_valid:
                        yield pinyin

    def _get_consonant_list(self, consonants):
        try:
            consonants = ConsonantScheme(consonants)
        except NotARhymeSchemeError:
            # 'bpmf'
            return (Consonant(x) for x in consonants)
        except TypeError:
            # ('b', 'p', 'm', 'f') or ('FAMILY', 'b', 'p', 'm', 'f')
            return itertools.chain.from_iterable(
                self._get_consonant_list(x) for x in consonants
            )
        else:
            match consonants:
                case ConsonantScheme.ALL:
                    return Consonant.all()
                case ConsonantScheme.FAMILY:
                    return self.consonant.all_family()

    def _get_vowel_list(self, vowels):
        try:
            vowels = VowelScheme(vowels)
        except NotARhymeSchemeError:
            return (Vowel(x) for x in re.split(r'[\s\t,]+', vowels))
        except TypeError:
            return itertools.chain.from_iterable(
                self._get_vowel_list(x) for x in vowels
            )
        else:
            return self.vowel.rhyme(vowels)

    def _get_tone_list(self, tones):
        if tones == 'ALL':
            return range(1, 6)
        return tones
