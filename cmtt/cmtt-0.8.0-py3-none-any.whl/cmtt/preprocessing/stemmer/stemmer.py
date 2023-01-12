
import re

from abc import ABCMeta, abstractmethod

class StemmerI(metaclass=ABCMeta):
    """
    A processing interface for removing morphological affixes from
    words.  This process is known as stemming.
    """

    @abstractmethod
    def stem(self, token):
        """
        Strip affixes from the token and return the stem.
        :param token: The token that should be stemmed.
        :type token: str
        """

class PorterStemmer(StemmerI):
    STEM_EXTENSION = "STEM_EXTENSION"

    def __init__(self, mode=STEM_EXTENSION):
        if mode not in (
            self.STEM_EXTENSION
        ):
            raise ValueError(
                "Mode must be one of PorterStemmer.STEM_EXTENSION, "
            )

        self.mode = mode

        if self.mode == self.STEM_EXTENSION:
            irregular_forms = {
                "sky": ["sky", "skies"],
                "die": ["dying"],
                "lie": ["lying"],
                "tie": ["tying"],
                "news": ["news"],
                "inning": ["innings", "inning"],
                "outing": ["outings", "outing"],
                "canning": ["cannings", "canning"],
                "howe": ["howe"],
                "proceed": ["proceed"],
                "exceed": ["exceed"],
                "succeed": ["succeed"],
            }

            self.pool = {}
            for key in irregular_forms:
                for val in irregular_forms[key]:
                    self.pool[val] = key

        self.vowels = frozenset(["a", "e", "i", "o", "u"])

    def _is_consonant(self, word, i):
    
        if word[i] in self.vowels:
            return False
        if word[i] == "y":
            if i == 0:
                return True
            else:
                return not self._is_consonant(word, i - 1)
        return True

    def _measure(self, stem):
        
        cv_sequence = ""

        # Construct a string of 'c's and 'v's representing whether each
        # character in `stem` is a consonant or a vowel.
        # e.g.  'architecture' becomes 'vcccvcvccvcv'
        for i in range(len(stem)):
            if self._is_consonant(stem, i):
                cv_sequence += "c"
            else:
                cv_sequence += "v"

        # Count the number of 'vc' occurrences, which is equivalent to
        # the number of 'VC' occurrences in Porter's reduced form in the
        # docstring above, which is in turn equivalent to `m`
        return cv_sequence.count("vc")

    def _has_positive_measure(self, stem):
        return self._measure(stem) > 0

    def _contains_vowel(self, stem):
        """Returns True if stem contains a vowel, else False"""
        for i in range(len(stem)):
            if not self._is_consonant(stem, i):
                return True
        return False

    def _ends_double_consonant(self, word):
        """Implements condition *d from the paper
        Returns True if word ends with a double consonant
        """
        return (
            len(word) >= 2
            and word[-1] == word[-2]
            and self._is_consonant(word, len(word) - 1)
        )

    def _ends_cvc(self, word):
        """Implements condition *o from the paper
        From the paper:
            *o  - the stem ends cvc, where the second c is not W, X or Y
                  (e.g. -WIL, -HOP).
        """
        return (
            len(word) >= 3
            and self._is_consonant(word, len(word) - 3)
            and not self._is_consonant(word, len(word) - 2)
            and self._is_consonant(word, len(word) - 1)
            and word[-1] not in ("w", "x", "y")
        ) or (
            self.mode == self.STEM_EXTENSION
            and len(word) == 2
            and not self._is_consonant(word, 0)
            and self._is_consonant(word, 1)
        )

    def _replace_suffix(self, word, suffix, replacement):
        """Replaces `suffix` of `word` with `replacement"""
        assert word.endswith(suffix), "Given word doesn't end with given suffix"
        if suffix == "":
            return word + replacement
        else:
            return word[: -len(suffix)] + replacement

    def _apply_rule_list(self, word, rules):
        """Suffix-removal rule to the word (in 3-tuples - suffix, word, condition)
        """
        for rule in rules:
            suffix, replacement, condition = rule
            if suffix == "*d" and self._ends_double_consonant(word):
                stem = word[:-2]
                if condition is None or condition(stem):
                    return stem + replacement
                else:
                    # Don't try any further rules
                    return word
            if word.endswith(suffix):
                stem = self._replace_suffix(word, suffix, "")
                if condition is None or condition(stem):
                    return stem + replacement
                else:
                    # Don't try any further rules
                    return word

        return word

    def _step1a(self, word):
        if self.mode == self.STEM_EXTENSION:
            if word.endswith("ies") and len(word) == 4:
                return self._replace_suffix(word, "ies", "ie")

        return self._apply_rule_list(
            word,
            [
                ("sses", "ss", None),  # SSES -> SS
                ("ies", "i", None),  # IES  -> I
                ("ss", "ss", None),  # SS   -> SS
                ("s", "", None),  # S    ->
            ],
        )

    def _step1b(self, word):
        """
            (m>0) EED -> EE                    feed      ->  feed
                                               agreed    ->  agree
            (*v*) ED  ->                       plastered ->  plaster
                                               bled      ->  bled
            (*v*) ING ->                       motoring  ->  motor
                                               sing      ->  sing
        
            AT -> ATE                       conflat(ed)  ->  conflate
            BL -> BLE                       troubl(ed)   ->  trouble
            IZ -> IZE                       siz(ed)      ->  size
            (*d and not (*L or *S or *Z))
               -> single letter
                                            hopp(ing)    ->  hop
                                            tann(ed)     ->  tan
            (m=1 and *o) -> E               fail(ing)    ->  fail
                                            fil(ing)     ->  file
        The rule to map to a single letter causes the removal of one of
        the double letter pair. The -E is put back on -AT, -BL and -IZ,
        so that the suffixes -ATE, -BLE and -IZE can be recognised
        later. This E may be removed in step 4.
        """
        if self.mode == self.STEM_EXTENSION:
            if word.endswith("ied"):
                if len(word) == 4:
                    return self._replace_suffix(word, "ied", "ie")
                else:
                    return self._replace_suffix(word, "ied", "i")

        # (m>0) EED -> EE
        if word.endswith("eed"):
            stem = self._replace_suffix(word, "eed", "")
            if self._measure(stem) > 0:
                return stem + "ee"
            else:
                return word

        rule_2_or_3_succeeded = False

        for suffix in ["ed", "ing"]:
            if word.endswith(suffix):
                intermediate_stem = self._replace_suffix(word, suffix, "")
                if self._contains_vowel(intermediate_stem):
                    rule_2_or_3_succeeded = True
                    break

        if not rule_2_or_3_succeeded:
            return word

        return self._apply_rule_list(
            intermediate_stem,
            [
                ("at", "ate", None),  # AT -> ATE
                ("bl", "ble", None),  # BL -> BLE
                ("iz", "ize", None),  # IZ -> IZE
                # (*d and not (*L or *S or *Z))
                # -> single letter
                (
                    "*d",
                    intermediate_stem[-1],
                    lambda stem: intermediate_stem[-1] not in ("l", "s", "z"),
                ),
                # (m=1 and *o) -> E
                (
                    "",
                    "e",
                    lambda stem: (self._measure(stem) == 1 and self._ends_cvc(stem)),
                ),
            ],
        )

    def _step1c(self, word):
        """
            (*v*) Y -> I                    happy        ->  happi
                                            sky          ->  sky
        """

        def nltk_condition(stem):
            """
            y->i is only done when y is preceded by a consonant,
            but not if the stem is only a single consonant, i.e.
               (*c and not c) Y -> I
            So 'happy' -> 'happi', but
               'enjoy' -> 'enjoy'  etc
            """
            return len(stem) > 1 and self._is_consonant(stem, len(stem) - 1)

        def original_condition(stem):
            return self._contains_vowel(stem)

        return self._apply_rule_list(
            word,
            [("y", "i",
                    nltk_condition
                    if self.mode == self.STEM_EXTENSION
                    else original_condition,
                )
            ],
        )

    def _step2(self, word):
        """
            (m>0) ATIONAL ->  ATE       relational     ->  relate
            (m>0) TIONAL  ->  TION      conditional    ->  condition
            (m>0) OUSNESS ->  OUS       callousness    ->  callous
            (m>0) ALITI   ->  AL        formaliti      ->  formal
            (m>0) IVITI   ->  IVE       sensitiviti    ->  sensitive
            (m>0) BILITI  ->  BLE       sensibiliti    ->  sensible
        """

        if self.mode == self.STEM_EXTENSION:
            # Instead of applying the ALLI -> AL rule after '(a)bli' per
            # the published algorithm, instead we apply it first, and,
            # if it succeeds, run the result through step2 again.
            if word.endswith("alli") and self._has_positive_measure(
                self._replace_suffix(word, "alli", "")
            ):
                return self._step2(self._replace_suffix(word, "alli", "al"))

        bli_rule = ("bli", "ble", self._has_positive_measure)
        abli_rule = ("abli", "able", self._has_positive_measure)

        rules = [
            ("ational", "ate", self._has_positive_measure),
            ("tional", "tion", self._has_positive_measure),
            ("enci", "ence", self._has_positive_measure),
            ("anci", "ance", self._has_positive_measure),
            ("izer", "ize", self._has_positive_measure),
            ("alli", "al", self._has_positive_measure),
            ("entli", "ent", self._has_positive_measure),
            ("eli", "e", self._has_positive_measure),
            ("ousli", "ous", self._has_positive_measure),
            ("ization", "ize", self._has_positive_measure),
            ("ation", "ate", self._has_positive_measure),
            ("ator", "ate", self._has_positive_measure),
            ("alism", "al", self._has_positive_measure),
            ("iveness", "ive", self._has_positive_measure),
            ("fulness", "ful", self._has_positive_measure),
            ("ousness", "ous", self._has_positive_measure),
            ("aliti", "al", self._has_positive_measure),
            ("iviti", "ive", self._has_positive_measure),
            ("biliti", "ble", self._has_positive_measure),
        ]

        if self.mode == self.STEM_EXTENSION:
            rules.append(("fulli", "ful", self._has_positive_measure))

            # The 'l' of the 'logi' -> 'log' rule is put with the stem,
            # so that short stems like 'geo' 'theo' etc work like
            # 'archaeo' 'philo' etc.
            rules.append(
                ("logi", "log", lambda stem: self._has_positive_measure(word[:-3]))
            )
        return self._apply_rule_list(word, rules)

    def _step3(self, word):
        """
            (m>0) ICATE ->  IC              triplicate     ->  triplic
            (m>0) ATIVE ->                  formative      ->  form
            (m>0) NESS  ->                  goodness       ->  good
        """
        return self._apply_rule_list(
            word,
            [
                ("icate", "ic", self._has_positive_measure),
                ("ative", "", self._has_positive_measure),
                ("alize", "al", self._has_positive_measure),
                ("iciti", "ic", self._has_positive_measure),
                ("ical", "ic", self._has_positive_measure),
                ("ful", "", self._has_positive_measure),
                ("ness", "", self._has_positive_measure),
            ],
        )

    def _step4(self, word):
        """
            (m>1) AL    ->                  revival        ->  reviv
            (m>1) ANCE  ->                  allowance      ->  allow
            (m>1) ENCE  ->                  inference      ->  infer
            (m>1) ER    ->                  airliner       ->  airlin
            (m>1) IC    ->                  gyroscopic     ->  gyroscop
            (m>1) ABLE  ->                  adjustable     ->  adjust
            (m>1) IBLE  ->                  defensible     ->  defens
            (m>1) ANT   ->                  irritant       ->  irrit
            (m>1) EMENT ->                  replacement    ->  replac
            (m>1) MENT  ->                  adjustment     ->  adjust
            (m>1) ENT   ->                  dependent      ->  depend
            (m>1 and (*S or *T)) ION ->     adoption       ->  adopt
            (m>1) OU    ->                  homologou      ->  homolog
            (m>1) ISM   ->                  communism      ->  commun
            (m>1) ATE   ->                  activate       ->  activ
            (m>1) ITI   ->                  angulariti     ->  angular
            (m>1) OUS   ->                  homologous     ->  homolog
            (m>1) IVE   ->                  effective      ->  effect
            (m>1) IZE   ->                  bowdlerize     ->  bowdler
        The suffixes are now removed. All that remains is a little
        tidying up.
        """
        measure_gt_1 = lambda stem: self._measure(stem) > 1

        return self._apply_rule_list(
            word,
            [
                ("al", "", measure_gt_1),
                ("ance", "", measure_gt_1),
                ("ence", "", measure_gt_1),
                ("er", "", measure_gt_1),
                ("ic", "", measure_gt_1),
                ("able", "", measure_gt_1),
                ("ible", "", measure_gt_1),
                ("ant", "", measure_gt_1),
                ("ement", "", measure_gt_1),
                ("ment", "", measure_gt_1),
                ("ent", "", measure_gt_1),
                # (m>1 and (*S or *T)) ION ->
                (
                    "ion",
                    "",
                    lambda stem: self._measure(stem) > 1 and stem[-1] in ("s", "t"),
                ),
                ("ou", "", measure_gt_1),
                ("ism", "", measure_gt_1),
                ("ate", "", measure_gt_1),
                ("iti", "", measure_gt_1),
                ("ous", "", measure_gt_1),
                ("ive", "", measure_gt_1),
                ("ize", "", measure_gt_1),
            ],
        )

    def _step5a(self, word):
        """Implements Step 5a from "An algorithm for suffix stripping"
        From the paper:
        Step 5a
            (m>1) E     ->                  probate        ->  probat
                                            rate           ->  rate
            (m=1 and not *o) E ->           cease          ->  ceas
        """
        if word.endswith("e"):
            stem = self._replace_suffix(word, "e", "")
            if self._measure(stem) > 1:
                return stem
            if self._measure(stem) == 1 and not self._ends_cvc(stem):
                return stem
        return word

    def _step5b(self, word):
        """Implements Step 5a from "An algorithm for suffix stripping"
        From the paper:
        Step 5b
            (m > 1 and *d and *L) -> single letter
                                    controll       ->  control
                                    roll           ->  roll
        """
        return self._apply_rule_list(
            word, [("ll", "l", lambda stem: self._measure(word[:-1]) > 1)]
        )

    def stem(self, sentence, to_lowercase=True):
        """
        :param to_lowercase: if `to_lowercase=True` the word always lowercase
        """
        words = sentence.split()
        stemmed_sentence = []
        for word in words:
            stem = word.lower() if to_lowercase else word

            if self.mode == self.STEM_EXTENSION and word in self.pool:
                return self.pool[stem]

            if len(word) <= 2:
                stemmed_sentence.append(stem)

            else:
                stem = self._step1a(stem)
                stem = self._step1b(stem)
                stem = self._step1c(stem)
                stem = self._step2(stem)
                stem = self._step3(stem)
                stem = self._step4(stem)
                stem = self._step5a(stem)
                stem = self._step5b(stem)

                stemmed_sentence.append(stem)
    
        str_stemmed_sentence = " ".join(stemmed_sentence)

        return str_stemmed_sentence

    def __repr__(self):
        return "<PorterStemmer>"
