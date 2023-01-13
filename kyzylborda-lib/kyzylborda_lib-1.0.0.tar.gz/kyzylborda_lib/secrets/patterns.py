from __future__ import annotations

import abc
import re
import string
from typing import Optional


try:
    from re import _parser as sre_parse
except ImportError:
    import sre_parse


__all__ = ("PatternGenerator",)


class SubPattern(abc.ABC):
    def __init__(self):
        self._entropy_space = None
        self._regex = None
        self._patterned_regex = None

    @abc.abstractmethod
    def generate(self, entropy: int) -> str:
        ...

    @abc.abstractmethod
    def _get_entropy_space(self) -> int:
        ...

    def get_entropy_space(self) -> int:
        if self._entropy_space is None:
            self._entropy_space = self._get_entropy_space()
        return self._entropy_space

    @abc.abstractmethod
    def _get_regex(self) -> str:
        ...

    def get_regex(self) -> str:
        if self._regex is None:
            self._regex = self._get_regex()
        return self._regex

    @abc.abstractmethod
    def _get_patterned_regex(self) -> str:
        ...

    def get_patterned_regex(self) -> re.Pattern:
        if self._patterned_regex is None:
            self._patterned_regex = re.compile(self._get_patterned_regex())
        return self._patterned_regex

    @abc.abstractmethod
    def extract_entropy(self, string: str) -> int:
        ...


class ConcatSubPattern(SubPattern):
    def __init__(self, parts: list[SubPattern]):
        super().__init__()
        self.parts = parts

    def generate(self, entropy: int) -> str:
        result = []
        for part in self.parts:
            part_entropy_space = part.get_entropy_space()
            entropy, part_entropy = divmod(entropy, part_entropy_space)
            result.append(part.generate(part_entropy))
        assert entropy == 0
        return "".join(result)

    def _get_entropy_space(self) -> int:
        entropy_space = 1
        for part in self.parts:
            entropy_space *= part.get_entropy_space()
        return entropy_space

    def _get_regex(self) -> str:
        return "".join(part.get_regex() for part in self.parts)

    def _get_patterned_regex(self) -> str:
        return "".join(rf"({part.get_regex()})" for part in self.parts)

    def extract_entropy(self, string: str) -> int:
        re_match = self.get_patterned_regex().fullmatch(string)
        assert re_match is not None
        entropy = 0
        coeff = 1
        for i, part in enumerate(self.parts):
            entropy += part.extract_entropy(re_match.group(i + 1)) * coeff
            coeff *= part.get_entropy_space()
        return entropy


class EitherSubPattern(SubPattern):
    def __init__(self, options: list[SubPattern]):
        super().__init__()
        self.options = options

    def generate(self, entropy: int) -> str:
        for option in self.options:
            option_entropy_space = option.get_entropy_space()
            if entropy < option_entropy_space:
                return option.generate(entropy)
            entropy -= option_entropy_space
        assert False

    def _get_entropy_space(self) -> int:
        return sum(option.get_entropy_space() for option in self.options)

    def _get_regex(self) -> str:
        return "(?:" + "|".join(option.get_regex() for option in self.options) + ")"

    def _get_patterned_regex(self) -> str:
        return "|".join(rf"({option.get_regex()})" for option in self.options)

    def extract_entropy(self, string: str) -> int:
        re_match = self.get_patterned_regex().fullmatch(string)
        assert re_match is not None
        entropy = 0
        for i, option in enumerate(self.options):
            if re_match.group(i + 1) is not None:
                return entropy + option.extract_entropy(re_match.group(i + 1))
            entropy += option.get_entropy_space()
        assert False


class LiteralSubPattern(SubPattern):
    def __init__(self, string: str):
        super().__init__()
        self.string = string

    def generate(self, entropy: int) -> str:
        assert entropy == 0
        return self.string

    def _get_entropy_space(self) -> int:
        return 1

    def _get_regex(self) -> str:
        return re.escape(self.string)

    def _get_patterned_regex(self) -> str:
        return ""

    def extract_entropy(self, string: str) -> int:
        assert string == self.string
        return 0


class RepeatSubPattern(SubPattern):
    def __init__(self, min: int, max: int, pattern: SubPattern):
        super().__init__()
        self.min = min
        self.max = max
        self.pattern = pattern

    def generate(self, entropy: int) -> str:
        # TODO: optimize this?
        pattern_entropy_space = self.pattern.get_entropy_space()
        for length in range(self.min, self.max + 1):
            cnt = pattern_entropy_space ** length
            if entropy >= cnt:
                entropy -= cnt
                continue
            result = []
            for i in range(length):
                entropy, pattern_entropy = divmod(entropy, pattern_entropy_space)
                result.append(self.pattern.generate(pattern_entropy))
            assert entropy == 0
            return "".join(result)
        assert False

    def _get_entropy_space(self) -> int:
        pattern_entropy_space = self.pattern.get_entropy_space()
        # TODO: optimize this?
        return sum(pattern_entropy_space ** n for n in range(self.min, self.max + 1))

    def _get_regex(self) -> str:
        return f"(?:{self.pattern._get_regex()}){{{self.min},{self.max}}}"

    def _get_patterned_regex(self) -> str:
        pattern_regex = self.pattern.get_regex()
        regex = ""
        for _ in range(self.min, self.max):
            regex = f"(?:|({pattern_regex}){regex})"
        return f"({pattern_regex})" * self.min + regex

    def extract_entropy(self, string: str) -> int:
        pattern_entropy_space = self.pattern.get_entropy_space()

        re_match = self.get_patterned_regex().fullmatch(string)
        assert re_match is not None

        length = sum(re_match.group(i + 1) is not None for i in range(self.max))

        # TODO: optimize this?
        entropy = sum(pattern_entropy_space ** n for n in range(self.min, length))

        coeff = 1
        for i in range(length):
            entropy += self.pattern.extract_entropy(re_match.group(i + 1)) * coeff
            coeff *= pattern_entropy_space
        return entropy


def sre_sub_pattern_to_sub_pattern(sre_sub_pattern: sre_parse.SubPattern) -> SubPattern:
    def parse_one(op: int, arg) -> SubPattern:
        if op is sre_parse.IN:
            options = [parse_one(op1, arg1) for op1, arg1 in arg]
            return options[0] if len(options) == 0 else EitherSubPattern(options)
        elif op is sre_parse.LITERAL:
            return LiteralSubPattern(chr(arg))
        elif op is sre_parse.CATEGORY:
            if arg is sre_parse.CATEGORY_DIGIT:
                options = string.digits
            elif arg is sre_parse.CATEGORY_SPACE:
                options = string.whitespace
            elif arg is sre_parse.CATEGORY_WORD:
                options = string.ascii_letters + string.digits + "_"
            elif arg is (sre_parse.CATEGORY_NOT_DIGIT, sre_parse.CATEGORY_NOT_SPACE, sre_parse.CATEGORY_NOT_WORD):
                raise ValueError("Negative sets are not allowed")
            else:
                raise ValueError(f"Unknown category {arg}")
            return EitherSubPattern([LiteralSubPattern(c) for c in options])
        elif op is sre_parse.ANY:
            raise ValueError("Universal quantifier is not allowed")
        elif op in (sre_parse.MAX_REPEAT, sre_parse.MIN_REPEAT):
            min_cnt, max_cnt, item = arg
            if max_cnt is None:
                raise ValueError("Unbounded repetition is not allowed")
            return RepeatSubPattern(min_cnt, max_cnt, sre_sub_pattern_to_sub_pattern(item))
        elif op is sre_parse.BRANCH:
            options = [sre_sub_pattern_to_sub_pattern(option) for option in arg[1]]
            return options[0] if len(options) == 1 else EitherSubPattern(options)
        elif op is sre_parse.SUBPATTERN:
            return sre_sub_pattern_to_sub_pattern(arg[3] if len(arg) >= 4 else arg[1])
            (group, add_flags, del_flags, p)
        elif op is sre_parse.AT:
            raise ValueError("Location quantifiers are not allowed")
        elif op is sre_parse.NOT_LITERAL:
            raise ValueError("Negative sets are not allowed")
        elif op is sre_parse.GROUPREF:
            raise ValueError("Backward references are not allowed")
        elif op is sre_parse.RANGE:
            first, last = arg
            return EitherSubPattern([LiteralSubPattern(chr(n)) for n in range(first, last + 1)])
            raise ValueError("Backward references are not allowed")
        else:
            raise ValueError(f"Unknown regular expression opcode {op}")

    if not sre_sub_pattern:
        return LiteralSubPattern("")

    parts = [parse_one(op, arg) for op, arg in sre_sub_pattern.data]
    return parts[0] if len(parts) == 1 else ConcatSubPattern(parts)


class PatternGenerator:
    def __init__(self, format: str):
        self.pattern: SubPattern = sre_sub_pattern_to_sub_pattern(sre_parse.parse(format))
        self.regex = None

    def get_entropy_space(self) -> int:
        return self.pattern.get_entropy_space()

    def generate(self, entropy: int) -> str:
        return self.pattern.generate(entropy)

    def extract_entropy(self, secret: str) -> Optional[int]:
        if self.regex is None:
            self.regex = re.compile(self.pattern.get_regex())
        if self.regex.fullmatch(secret) is None:
            return None
        return self.pattern.extract_entropy(secret)

    # Inefficient. For unit tests only
    def _list_all(self):
        return [self.generate(i) for i in range(self.get_entropy_space())]


def _test():
    assert PatternGenerator("")._list_all() == [""]
    assert PatternGenerator("a")._list_all() == ["a"]
    assert PatternGenerator("a|b|xx")._list_all() == ["a", "b", "xx"]
    assert PatternGenerator("[abc]")._list_all() == ["a", "b", "c"]
    assert PatternGenerator("(a|b)(c|d)")._list_all() == ["ac", "bc", "ad", "bd"]
    assert PatternGenerator("(a|b|c)(d|e|f)")._list_all() == ["ad", "bd", "cd", "ae", "be", "ce", "af", "bf", "cf"]
    assert PatternGenerator("(a|b)(c|d)|e")._list_all() == ["ac", "bc", "ad", "bd", "e"]
    assert PatternGenerator("a{2,5}")._list_all() == ["aa", "aaa", "aaaa", "aaaaa"]
    assert PatternGenerator("a{2,3}b{1,2}")._list_all() == ["aab", "aaab", "aabb", "aaabb"]
    assert PatternGenerator("(a|b){1,3}")._list_all() == ["a", "b", "aa", "ba", "ab", "bb", "aaa", "baa", "aba", "bba", "aab", "bab", "abb", "bbb"]

    for pattern in ["", "a", "a|b|xx", "[abc]", "(a|b)(c|d)", "(a|b|c)(d|e|f)", "(a|b)(c|d)|e", "a{2,5}", "a{2,3}b{1,2}", "(a|b){1,3}"]:
        gen = PatternGenerator(pattern)
        for entropy, string in enumerate(gen._list_all()):
            assert gen.extract_entropy(string) == entropy

    assert PatternGenerator("a").extract_entropy("b") is None


_test()
