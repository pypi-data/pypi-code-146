"""Test voice
"""
# NOTE: since these tests use sqlite as their DB backend, indexes for results
# start at 1. This may differ if using postgresql in actual use.

# pylint: disable=missing-function-docstring,disable=missing-class-docstring
# pylint: disable=too-few-public-methods
# TODO: This isn't great and implies some re-architecting is needed
# pylint: disable=protected-access
import sys
from pathlib import Path

import pytest
import sqlalchemy

import hlvox

from . import utils as th

# Stand-in files for testing
normal_files = ["hello.wav", "my.wav", "name.wav", "is.wav", "vox.wav"]
inconst_format_files = ["hello.mp3", "my.wav", "name", "is.wav", "vox.mp4"]
no_format_files = ["imatextfile", "whatami"]
alph_files = ["a.wav", "b.wav", "c.wav"]
category_files = {'bad': ["stop.wav", "bad.wav",
                          "no.wav"], 'good': ["go.wav", "yes.wav"]}


class TestFileHandling():
    def test_empty_files(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, [])
        with pytest.raises(hlvox.NoWordsFound):
            hlvox.SingleVoice(name='test', path=voice_dir,
                              database=None)

    def test_inconsistent_format(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, inconst_format_files)
        with pytest.raises(hlvox.InconsistentAudioFormats):
            hlvox.SingleVoice(name='test', path=voice_dir,
                              database=None)

    def test_no_format(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, no_format_files)
        with pytest.raises(hlvox.NoAudioFormatFound):
            hlvox.SingleVoice(name='test', path=voice_dir,
                              database=None)

    def test_audio_format(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, normal_files)
        with hlvox.SingleVoice(name='test', path=voice_dir, database=None) as unit:
            assert unit.get_audio_format() == "wav"


class TestDictContents():
    def test_basic_dict(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, normal_files)

        expected_names = [name[:-4] for name in normal_files]
        expected_names.sort()

        with hlvox.SingleVoice(name='test', path=voice_dir, database=None) as unit:
            assert expected_names == unit.words

    def test_alphab(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, alph_files)

        expected_names = ["a", "b", "c"]

        with hlvox.SingleVoice(name='test', path=voice_dir, database=None) as unit:
            assert expected_names == unit.words

    def test_caps(self, tmp_path: Path):
        words = [
            "Cap.wav",
            "Cappa.wav",
        ]
        voice_dir = th.create_voice_files(tmp_path, words)

        expected_names = ["cap", "cappa"]

        with hlvox.SingleVoice(name='test', path=voice_dir, database=None) as unit:
            assert expected_names == unit.words

    def test_categories(self, tmp_path: Path):
        voice_dir = th.create_category_files(tmp_path, category_files)
        expected_names = [item[:-4]
                          for sublist in category_files.values() for item in sublist]
        expected_names.sort()
        with hlvox.SingleVoice(name='test', path=voice_dir, database=None) as unit:
            assert expected_names == unit.words

            for category, words in category_files.items():
                category_words = [word[:-4] for word in words]
                category_words.sort()
                assert unit.categories[category] == category_words

    @pytest.mark.skipif(sys.platform == "win32", reason="Windows is not case sensitive so duplicates cant exist")
    def test_duplicates(self, tmp_path: Path):
        words = [
            "Cap.wav",
            "cAP.wav",
        ]
        voice_dir = th.create_voice_files(tmp_path, words, touch_only=True)

        with pytest.raises(hlvox.DuplicateWords):
            hlvox.SingleVoice(name='test', path=voice_dir,
                              database=None)


class TestDatabase():
    def test_reuse(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, normal_files)
        database = sqlalchemy.create_engine(f'sqlite:///{tmp_path}/db.sqlite')
        voice = hlvox.SingleVoice(
            name='test', path=voice_dir, database=database)

        voice.generate_audio(sentence="hello hello")
        voice.exit()

        voice = hlvox.SingleVoice(
            name='test', path=voice_dir, database=database)
        assert voice.get_generated_sentences() == ["hello hello"]


@pytest.fixture(name="voice")
def voice_fixture(tmp_path: Path):
    voice_dir = th.create_voice_files(tmp_path, normal_files)
    database = sqlalchemy.create_engine(f'sqlite:///{tmp_path}/db.sqlite')
    voice = hlvox.SingleVoice(
        name='test', path=voice_dir, database=database)
    yield voice
    voice.exit()


class TestSayableUnsayable():
    def test_empty_sent(self, voice: hlvox.SingleVoice):
        ret_say, ret_unsay = voice.get_sayable_unsayable([])

        assert ret_say == []
        assert ret_unsay == []

    def test_simple_sent(self, voice: hlvox.SingleVoice):
        words = ["hello"]
        ret_say, ret_unsay = voice.get_sayable_unsayable(words)

        assert ret_say == ["hello"]
        assert ret_unsay == []

    def test_duplicates(self, voice: hlvox.SingleVoice):
        words = ["hello", "hello", "world", "world", ",",
                 ",", ".", ".", "duplicates!", "duplicates"]

        ret_say, ret_unsay = voice.get_sayable_unsayable(words)

        assert not set(ret_say) ^ set(["hello", ",", "."])
        assert not set(ret_unsay) ^ set(["world", "duplicates", "duplicates!"])

    def test_comp_sent(self, voice: hlvox.SingleVoice):
        words = ["hello", ",", "world", ".", "vox",
                 "can't", "say", "some", "of", "this", "."]

        ret_say, ret_unsay = voice.get_sayable_unsayable(words)

        assert not set(ret_say) ^ set(["hello", ",", "vox", "."])
        assert not set(ret_unsay) ^ set(
            ["world", "can't", "say", "some", "of", "this"]
        )

    def test_dup_punct(self, voice: hlvox.SingleVoice):
        words = ["hello", ".", ".", ".", "world"]

        ret_say, ret_unsay = voice.get_sayable_unsayable(words)

        assert not set(ret_say) ^ set(["hello", "."])
        assert not set(ret_unsay) ^ set(["world"])


class TestSentenceGeneration():
    def test_empty_sent(self, voice: hlvox.SingleVoice):
        ret = voice.generate_audio("")

        assert ret.sentence == ""
        assert ret.sayable == []
        assert ret.unsayable == []
        assert ret.audio is None

        assert voice.get_generated_sentences_dict() == {}

    def test_unsayable_sent(self, voice: hlvox.SingleVoice):
        ret = voice.generate_audio("whatthefuckdidyoujustsaytome")

        assert ret.sentence == ""
        assert ret.sayable == []
        assert ret.unsayable == ["whatthefuckdidyoujustsaytome"]
        assert ret.audio is None

        assert voice.get_generated_sentences_dict() == {}

    def test_sayable_sent(self, voice: hlvox.SingleVoice):
        sentence = "hello, my name is vox"
        ret = voice.generate_audio(sentence)

        assert ret.sentence == "hello , my name is vox"
        assert ret.sayable == [",", "hello", "is", "my", "name", "vox"]
        assert ret.unsayable == []
        assert ret.audio is not None

        assert voice.get_generated_sentences_dict() == {
            1: "hello , my name is vox"}

    def test_duplicate_sent(self, voice: hlvox.SingleVoice):
        voice.generate_audio("hello hello")
        voice.generate_audio("hello hello")

        assert voice.get_generated_sentences_dict() == {1: "hello hello"}
        assert len(voice._get_generated_sentences_list()) == 1

    def test_duplicate_words(self, voice: hlvox.SingleVoice):
        ret = voice.generate_audio("hello hello hello")

        assert ret.sentence == "hello hello hello"
        assert ret.sayable == ["hello"]
        assert ret.unsayable == []
        assert ret.audio is not None

    def test_dup_punct(self, voice: hlvox.SingleVoice):
        ret = voice.generate_audio("hello... hello")

        assert ret.sentence == "hello . . . hello"
        assert ret.sayable == [".", "hello"]
        assert ret.unsayable == []
        assert ret.audio is not None

    def test_multiple_sent(self, voice: hlvox.SingleVoice):
        voice.generate_audio("hello hello")
        voice.generate_audio("vox hello")

        assert voice.get_generated_sentences_dict() == {
            1: "hello hello",
            2: "vox hello",
        }

    def test_dry_run(self, voice: hlvox.SingleVoice):
        ret = voice.generate_audio("hello", dry_run=True)
        assert ret.audio is None

    def test_one_word(self, voice: hlvox.SingleVoice):
        # We don't bother saving single words to the database
        voice.generate_audio("hello")

        assert voice.get_generated_sentences_dict() == {}


class TestGetGeneratedSentences():
    def test_no_sentences(self, voice: hlvox.SingleVoice):
        ret = voice.get_generated_sentences()

        assert ret == []

    def test_single_sentences(self, voice: hlvox.SingleVoice):
        voice.generate_audio("hello hello")

        ret = voice.get_generated_sentences()

        assert ret == ["hello hello"]

    def test_multiple_sentences(self, voice: hlvox.SingleVoice):
        voice.generate_audio("hello hello")
        voice.generate_audio("vox hello")

        ret = voice.get_generated_sentences()

        assert ret == ["hello hello", "vox hello"]


class TestGetGeneratedSentencesDict():
    def test_no_sentences(self, voice: hlvox.SingleVoice):
        ret = voice.get_generated_sentences_dict()

        assert ret == {}

    def test_single_sentences(self, voice: hlvox.SingleVoice):
        voice.generate_audio("hello hello")

        ret = voice.get_generated_sentences_dict()

        assert ret == {1: "hello hello"}

    def test_multiple_sentences(self, voice: hlvox.SingleVoice):
        voice.generate_audio("hello hello")
        voice.generate_audio("vox hello")

        ret = voice.get_generated_sentences_dict()

        assert ret == {1: "hello hello", 2: "vox hello"}


@pytest.fixture(name="multi_voice")
def multi_voice_fixture(tmp_path: Path):
    norm_voice_dir = th.create_voice_files(
        tmp_path, normal_files, voice_name='norm')
    alph_voice_dir = th.create_voice_files(
        tmp_path, alph_files, voice_name='alph')
    alph_2_voice_dir = th.create_voice_files(
        tmp_path, alph_files, voice_name='alph2')
    norm_voice = hlvox.SingleVoice(
        name='norm',
        path=norm_voice_dir,
        database=sqlalchemy.create_engine(f'sqlite:///{tmp_path}/norm.sqlite')
    )
    alph_voice = hlvox.SingleVoice(
        name='alph',
        path=alph_voice_dir,
        database=sqlalchemy.create_engine(f'sqlite:///{tmp_path}/alph.sqlite')
    )
    alph_2_voice = hlvox.SingleVoice(
        name='alph2',
        path=alph_2_voice_dir,
        database=sqlalchemy.create_engine(f'sqlite:///{tmp_path}/alph2.sqlite')
    )
    voices = {
        'norm': norm_voice,
        'alph': alph_voice,
        'alph2': alph_2_voice,
    }
    multi_voice = hlvox.MultiVoice(
        voices=voices,
        database=sqlalchemy.create_engine(f'sqlite:///{tmp_path}/multi.sqlite'),
    )
    yield multi_voice
    multi_voice.exit()
    for voice in voices.values():
        voice.exit()


EXPECTED_MULTI_VOICE_WORDS = [
    'norm:hello', 'norm:is', 'norm:my', 'norm:name',  'norm:vox',
    'alph:a', 'alph:b', 'alph:c',
    'alph2:a', 'alph2:b', 'alph2:c',
]

# Multi-voice tests


class TestMultiWords:
    def test_normal(self, multi_voice: hlvox.MultiVoice):
        assert multi_voice.words == EXPECTED_MULTI_VOICE_WORDS


class TestMultiProcessSentence:
    # Just want to check that punctuation works as expected
    def test_normal(self, multi_voice: hlvox.MultiVoice):
        words = ["norm:hello", ",", "norm:my",
                 "norm:name", "alph:a,", "alph2:b", "."]
        exp_words = ["norm:hello", ",", "norm:my",
                     "norm:name", "alph:a", ",", "alph2:b", "."]
        ret = multi_voice.process_sentence(words)
        assert ret == exp_words


class TestMultiSayableUnsayable:
    def test_empty(self, multi_voice: hlvox.MultiVoice):
        sayable, unsayable = multi_voice.get_sayable_unsayable(words=[])
        assert not sayable
        assert not unsayable

    def test_all_sayable(self, multi_voice: hlvox.MultiVoice):
        words = ["norm:hello", "norm:my", "alph:a", "alph2:a"]
        sayable, unsayable = multi_voice.get_sayable_unsayable(words=words)
        words.sort()
        assert sayable == words
        assert not unsayable

    def test_some_unsayable(self, multi_voice: hlvox.MultiVoice):
        exp_unsayable = ["norm:nope", "alph:butter", "alph2:404"]
        exp_sayable = ["norm:vox", "alph:c", "alph2:c"]
        words = exp_sayable + exp_unsayable
        sayable, unsayable = multi_voice.get_sayable_unsayable(words=words)
        exp_sayable.sort()
        exp_unsayable.sort()
        assert sayable == exp_sayable
        assert unsayable == exp_unsayable

    def test_punctuation(self, multi_voice: hlvox.MultiVoice):
        words = ["norm:hello", "norm:,", "alph:a", "alph2:."]
        words.sort()
        sayable, unsayable = multi_voice.get_sayable_unsayable(words=words)
        assert sayable == words
        assert not unsayable


class TestMultiWordVoiceAssignment:
    def test_empty(self, multi_voice: hlvox.MultiVoice):
        assert not multi_voice._get_word_voice_assignment(words=[])

    def test_no_initial_voice(self, multi_voice: hlvox.MultiVoice):
        words = ["hello", "norm:my"]

        with pytest.raises(hlvox.NoVoiceSpecified):
            multi_voice._get_word_voice_assignment(words=words)

    def test_normal(self, multi_voice: hlvox.MultiVoice):
        voices = multi_voice._voices
        words = ["norm:hello", "my", "alph:a", "a",
                 "alph2:a", "norm:vox", "is", "alph:b"]
        exp_words_and_voices = [
            ("hello", voices["norm"]),
            ("my", voices["norm"]),
            ("a", voices["alph"]),
            ("a", voices["alph"]),
            ("a", voices["alph2"]),
            ("vox", voices["norm"]),
            ("is", voices["norm"]),
            ("b", voices["alph"]),
        ]

        assert multi_voice._get_word_voice_assignment(
            words=words) == exp_words_and_voices

    def test_punctuation(self, multi_voice: hlvox.MultiVoice):
        voices = multi_voice._voices
        words = ["norm:hello", ",", "alph:a", "a",
                 ".", "alph2:a", "norm:vox", "is", "alph:b"]
        exp_words_and_voices = [
            ("hello", voices["norm"]),
            (",", voices["norm"]),
            ("a", voices["alph"]),
            ("a", voices["alph"]),
            (".", voices["alph"]),
            ("a", voices["alph2"]),
            ("vox", voices["norm"]),
            ("is", voices["norm"]),
            ("b", voices["alph"]),
        ]

        assert multi_voice._get_word_voice_assignment(
            words=words) == exp_words_and_voices


class TestMultiCombinedVoiceSentences:
    def test_empty(self, multi_voice: hlvox.MultiVoice):
        assert not multi_voice.get_combined_voice_sentences(
            words_and_voices=[])

    def test_single(self, multi_voice: hlvox.MultiVoice):
        voices = multi_voice._voices
        words_and_voices = [
            ("hello", voices["norm"])
        ]

        exp = [(voices["norm"], ["hello"])]
        assert multi_voice.get_combined_voice_sentences(
            words_and_voices=words_and_voices) == exp

    def test_multiple(self, multi_voice: hlvox.MultiVoice):
        voices = multi_voice._voices
        words_and_voices = [
            ("hello", voices["norm"]),
            ("my", voices["norm"]),
            ("a", voices["alph"]),
            ("a", voices["alph"]),
            ("a", voices["alph2"]),
            ("vox", voices["norm"]),
            ("is", voices["norm"]),
            ("b", voices["alph"]),
        ]

        exp = [
            (voices["norm"], ["hello", "my"]),
            (voices["alph"], ["a", "a"]),
            (voices["alph2"], ["a"]),
            (voices["norm"], ["vox", "is"]),
            (voices["alph"], ["b"]),
        ]
        assert multi_voice.get_combined_voice_sentences(
            words_and_voices=words_and_voices) == exp


class TestMultiGenerateAudio:
    def test_normal(self, multi_voice: hlvox.MultiVoice):
        sentence = "norm:hello, my name is vox. alph:a b c"
        ret = multi_voice.generate_audio(sentence=sentence)

        exp_sentence = "norm:hello , my name is vox . alph:a b c"
        assert ret.sentence == exp_sentence
        # Sentence should not be saved into the individual voice's database
        assert len(multi_voice._voices["norm"].get_generated_sentences()) == 0
        assert len(multi_voice._voices["alph"].get_generated_sentences()) == 0


class TestDifficultSentences:
    def test_ellipse(self, multi_voice: hlvox.MultiVoice):
        sentence = "norm:hello norm:. norm:. norm:."
        ret = multi_voice.generate_audio(sentence=sentence)

        exp_sentence = "norm:hello . . ."
        assert ret.sentence == exp_sentence

        sentence = "norm:hello..."
        ret = multi_voice.generate_audio(sentence=sentence)
        exp_sentence = "norm:hello . . ."
        assert ret.sentence == exp_sentence

    def test_start_ellipse(self, multi_voice: hlvox.MultiVoice):
        sentence = "norm:."
        ret = multi_voice.generate_audio(sentence=sentence)

        exp_sentence = "norm:."
        assert ret.sentence == exp_sentence

        sentence = "norm:. . ."
        ret = multi_voice.generate_audio(sentence=sentence)

        exp_sentence = "norm:. . ."
        assert ret.sentence == exp_sentence

        sentence = "norm:..."
        ret = multi_voice.generate_audio(sentence=sentence)
        assert ret.sentence == exp_sentence
