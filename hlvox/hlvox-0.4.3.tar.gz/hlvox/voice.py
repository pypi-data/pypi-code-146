"""Defines a unique voice
"""
import argparse
import json
import logging
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import sqlalchemy
from pydub import AudioSegment

log = logging.getLogger(__name__)


# How much delay should be added in place of punctuation (in milliseconds)
PUNCTUATION_TIMING = {
    ',': 250,
    '.': 500,
}

DB_NAME = 'db.json'


class NoWordsFound(Exception):
    """Raised when a voice has no words
    """


class DuplicateWords(Exception):
    """Raised when a voice has duplicate words
    """


class InconsistentAudioFormats(Exception):
    """Raised when words have inconsistent audio formats
    """


class NoAudioFormatFound(Exception):
    """Raised when no audio format can be found
    """


class FailedToSplit(Exception):
    """Raised when a sentence cannot be split
    """


class NoVoiceSpecified(Exception):
    """Raised when no voice is specified
    """


class NoDatabaseSpecified(Exception):
    """No database connection was specified during init
    """


@dataclass
class Sentence:
    """Represents a sentence and it's parts
    """
    sentence: str
    sayable: List[str]
    unsayable: List[str]
    audio: Optional[AudioSegment] = None


@dataclass
class DatabaseConnection:
    """Stores info related to database connection
    """
    engine: sqlalchemy.engine.Engine
    metadata: sqlalchemy.MetaData
    sentence_table: sqlalchemy.Table


class Voice:
    """Base class for Voice-like interfaces.
    Intended to involve generation of audio
    files from some source (files, web, etc).
    """

    def __init__(
        self,
        name: str,
        database: Optional[sqlalchemy.engine.Engine],
    ):
        self.name = name

        self._db: Optional[DatabaseConnection] = None
        if database is not None:
            metadata = sqlalchemy.MetaData()
            sentence_table = sqlalchemy.Table(
                self.name,
                metadata,
                sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                sqlalchemy.Column("sentence", sqlalchemy.String, unique=True, nullable=False),
            )
            metadata.create_all(database)
            self._db = DatabaseConnection(
                metadata=metadata,
                sentence_table=sentence_table,
                engine=database,
            )
        self.words: List[str] = []
        self.categories: Dict[str, List[str]] = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.exit()

    def exit(self):
        """Clean up and close voice
        """
        if self._db is not None:
            self._db.engine.dispose()

    def _insert_sentence_into_db(self, sentence: str):
        if self._db is None:
            raise NoDatabaseSpecified
        ins = self._db.sentence_table.insert().values(sentence=sentence)
        with self._db.engine.begin() as conn:
            conn.execute(ins)

    def _sentence_exists(self, sentence: str) -> bool:
        if self._db is None:
            raise NoDatabaseSpecified

        sel = self._db.sentence_table.select().where(self._db.sentence_table.c.sentence == sentence)
        with self._db.engine.connect() as conn:
            result = conn.execute(sel)
            # TODO: there should be a way to use `.Count()` here
            return bool(result.all())

    def _get_generated_sentences_list(self) -> list[str]:
        if self._db is None:
            raise NoDatabaseSpecified
        sel = self._db.sentence_table.select()
        with self._db.engine.connect() as conn:
            result = conn.execute(sel)
            return [r.sentence for r in result]

    def _get_generated_sentences_dict(self) -> dict[int, str]:
        if self._db is None:
            raise NoDatabaseSpecified
        sel = self._db.sentence_table.select()
        with self._db.engine.connect() as conn:
            result = conn.execute(sel)
            return {r.id: r.sentence for r in result}

    def _get_sentence_info(self, words: List[str]) -> Tuple[Sentence, List[str]]:
        """Get basic sentence info for a given
        split sentence.

        Args:
            words (List[str]): Words of sentence split into array

        Returns:
            Tuple[Sentence, List[str]]: Sentence info and sayable sentence array
        """
        sayable_words, unsayable_worlds = self.get_sayable_unsayable(words)
        sayable_sent_arr = self._get_sayable_sentence_arr(
            words, sayable_words)
        sayable_sent_str = self._create_sentence_string(sayable_sent_arr)

        sentence_info = Sentence(
            sentence=sayable_sent_str,
            sayable=sayable_words,
            unsayable=unsayable_worlds,
            audio=None,
        )
        return sentence_info, sayable_sent_arr

    def generate_audio_from_array(self, words: List[str], dry_run=False, save_to_db=True) -> Sentence:
        """Generates audio segment from sentence array.

        Args:
            words (List[str]): Words to try and turn into audio segment.
            dry_run (bool, optional): Skip actual segment generation. Defaults to False.

        Returns:
            Sentence: Sentence with audio segment.
        """
        sentence_info, sayable_sentence_array = self._get_sentence_info(
            words=words)

        if dry_run:
            return sentence_info

        log.debug("Generating %s", sentence_info.sentence)

        # Only create sentence if there are words to put in it
        if len(sentence_info.sayable) == 0:
            log.warning(
                "Can't say any words in %s, not generating", sentence_info.sentence)
            return sentence_info

        # Only bother inserting a sentence into the database if there is more than one word in it
        # TODO: test save_to_db
        if save_to_db and len(words) > 1:
            if not self._sentence_exists(sentence=sentence_info.sentence):
                self._insert_sentence_into_db(sentence=sentence_info.sentence)

        words_audio = self._create_audio_segments(sayable_sentence_array)

        sentence_info.audio = self.assemble_audio_segments(words_audio)

        return sentence_info

    def _create_audio_segments(
        self,
        word_array: List[str],  # pylint: disable=unused-argument
    ) -> List[AudioSegment]:
        """Create audio segments for each entry in an array of words.

        Args:
            word_array (List[str]): Words to turn into audio segments.

        Returns:
            List[AudioSegment]: Audio segments.
        """
        return []

    def generate_audio(self, sentence: str, dry_run=False) -> Sentence:
        """Generates audio from the given sentence

        Args:
            sentence (string): Sentence string to be generated
            dry_run (bool, optional): Don't generate audio. Defaults to False.
        Returns:
            Sentence: Information about generated sentence.
        """
        log.info("Asked to generate %s", sentence)
        split_sentence = self._split_sentence(sentence)
        proc_sentence = self.process_sentence(split_sentence)
        return self.generate_audio_from_array(
            words=proc_sentence,
            dry_run=dry_run,
        )

    @staticmethod
    def _split_sentence(sentence: str) -> List[str]:
        return sentence.lower().rstrip().split(" ")

    @staticmethod
    def process_sentence(split_sent: List[str]) -> List[str]:
        """
        Takes a normally formatted sentence and breaks it into base elements

        Args:
            split_sent (List[str]): words in sentence

        Returns:
            List[str]: array of elements in sentence
        """
        # TODO: This could use some rethinking. Should be easier to just always break punctuation marks
        # into their own elements, rather than selectively only dealing with trailing ones.
        log.info("Processing sentence '%s'", split_sent)

        # Pull out punctuation
        reduced_sent = []
        for item in split_sent:
            # find first punctuation mark, if any
            first_punct: Optional[str] = None
            try:
                first_punct = next(
                    (punct for punct in PUNCTUATION_TIMING if punct in item))
            except StopIteration:
                pass

            if first_punct:
                # Get its index
                first_punct_ind = item.find(first_punct)

                # Special case: If this is a multi voice sentence,
                # we don't want to rip the voice definition out of a singe-punctuation
                # mark. IE vox:.
                # TODO: This is a bit hacky. Would be great if this method doesn't
                # have to know about multi-voice syntax.
                if first_punct_ind >= 2 and item[first_punct_ind - 1] == ':':
                    reduced_sent.append(item[:first_punct_ind + 1])
                    if len(item) >= first_punct_ind:
                        first_punct_ind += 1
                else:
                    # Add everything before punct (the word, if any)
                    if item[:first_punct_ind]:
                        reduced_sent.append(item[:first_punct_ind])

                # Add all the punctuation if its actually punctuation
                # TODO: Figure out if I want to deal with types like ".hello" throwing out all the characters after the period.
                for punct in item[first_punct_ind:]:
                    if punct in PUNCTUATION_TIMING:
                        reduced_sent.append(punct)

            else:
                reduced_sent.append(item)

        # Clean blanks from reduced_sent
        if '' in reduced_sent:
            reduced_sent = [value for value in reduced_sent if value != '']

        log.info("Sentence processed: '%s'", reduced_sent)
        return reduced_sent

    def get_sayable_unsayable(self, words: List[str]) -> Tuple[List[str], List[str]]:
        """Get words that are sayable or unsayable
        from a list of words.

        Args:
            words (List[str]): Words to check.

        Returns:
            Tuple[List[str], List[str]]: Sayable and unsayable words.
        """
        # TODO: This shouldn't need two separate processings of the same sentence. Sets, people. Sets!
        sayable_words = self.words
        sayable_words_set = set(sayable_words)
        sayable_words_set.update(list(PUNCTUATION_TIMING.keys()))

        words_set = set((dict.fromkeys(words)))  # removes duplicates

        unsayable_set = words_set - sayable_words_set
        sayable_set = words_set - unsayable_set
        unsayable = list(unsayable_set)
        unsayable.sort()
        sayable = list(sayable_set)
        sayable.sort()
        return sayable, unsayable

    def _get_sayable_sentence_arr(self, words: List[str], sayable_words: List[str]) -> List[str]:
        """Removes words from sentence array that are not sayable.

        Args:
            words (List[str]): Array of words in sentence, in order.
            sayable_words (List[str]): Words from sentence that can actually be said.

        Returns:
            List[str]: Words in sentence that are sayable, in order.
        """
        # TODO: This is just a simple set operation. Function probably isn't needed. At least change to using a set.
        return [word for word in words if word in sayable_words]

    def _create_sentence_string(self, words: List[str]) -> str:
        """Joins sentence array into a string.

        Args:
            words (List[str]): Words in sentence, in order.

        Returns:
            str: Sentence string.
        """
        if len(words) == 1:
            return words[0]
        return " ".join(words)

    def get_generated_sentences(self) -> List[str]:
        """Gets the previously generated sentence strings

        Returns:
            List[str]: List of sentence strings generated previously
        """
        return self._get_generated_sentences_list()

    def get_generated_sentences_dict(self) -> Dict[int, str]:
        """Gets the previously generated sentence strings
        along with their corresponding ID in the database

        Returns:
            Dict[int, str]: Dict of sentence and id pairs
        """
        return self._get_generated_sentences_dict()

    @staticmethod
    def assemble_audio_segments(segments: List[AudioSegment]) -> AudioSegment:
        """Assemble audio segments into one audio segment.

        Args:
            segments (List[AudioSegment]): Segments to assemble.

        Returns:
            AudioSegment: Assembled audio segment.
        """
        # We set all audio segments to the lowest common frame rate
        # to avoid some really ugly artifacting when a low frame rate
        # clip is appended to a high frame rate one.
        frame_rates = [word.frame_rate for word in segments]
        frame_rate = min(frame_rates)

        sentence_audio = segments.pop(0)
        sentence_audio = sentence_audio.set_frame_rate(frame_rate)
        for word_audio in segments:
            word_audio = word_audio.set_frame_rate(frame_rate)
            sentence_audio = sentence_audio + word_audio

        return sentence_audio


class SingleVoice(Voice):
    """Comprises all information and methods
    needed to index a folder of voice audio files
    and generate audio from them given a sentence string.
    """

    def __init__(self, name: str, path: Path, database: Optional[DatabaseConnection]):
        """
        Args:
            name: Name of voice
            path (Path): Path to folder of voice audio files.
            database (Optional[DatabaseConnection]): Database connection information.
                If none provided, no database will be used and no data will persist.
        """
        super().__init__(name=name, database=database)
        self.path = path

        self.info_path = self.path.joinpath("info/")
        self.info_name = "info.json"

        self._word_dict, self.categories = self._build_word_dict(self.path)
        self._audio_format = self._find_audio_format(
            self._word_dict)  # TODO: Use properies?

        self.words = self._get_words()

        self._read_info(self.info_path, self.info_name)

    def _build_word_dict(self, path: Path) -> Tuple[Dict[str, Path], Dict[str, List[str]]]:
        """Builds dictionary of all available words and categories.

        Args:
            path (Path): Path to folder of voice audio files, or folders of voices files.

        Raises:
            DuplicateWords: Raised if there are duplicate filenames present.
            NoWordsFound: Raised if no words are found.

        Returns:
            Tuple[Dict[str, Path], Dict[str, List[str]]]: Dict of {filepath: word} associations and {category: [words]}.
        """
        word_dict = {}
        categories = defaultdict(list)

        for word_path in path.glob("**/*"):
            if word_path.is_dir():
                continue
            if word_path.parent.name == 'info':
                continue
            word = word_path
            name = str(word.stem).lower()
            if name in word_dict:
                raise DuplicateWords(f"Word {name} is duplicated")
            category = ''
            if word.parent != path:
                category = word.parent.name

            word_dict[name] = word
            if category:
                categories[category].append(name)
                # This is probably bad
                categories[category].sort()

        if len(word_dict) == 0:
            log.error("No words found")
            raise NoWordsFound

        return word_dict, categories

    def _read_info(self, path: Path, info_name: str):
        """Reads info file (if it exists)
        Args:
            path (Path): Path where info file resides.
            info_name (str): Name of info file.
        """
        # TODO: Allow arbitrary groupings of words
        info_path = path.joinpath(info_name)
        if info_path.exists():
            with open(info_path, 'r', encoding='UTF-8') as info_file:
                # TODO: we don't currently use this. Leaving it be to validate format
                json.load(info_file)

    def _find_audio_format(self, word_dict: Dict[str, Path]) -> str:
        """Determines audio format of voice audio files.

        Args:
            word_dict (Dict[str, Path]): Dict of {filepath: word} associations.

        Raises:
            NoAudioFormatFound: Raised if no audio format can be determined.
            InconsistentAudioFormats: Raised if there are inconsistent audio formats.

        Returns:
            str: Audio format.
        """
        file_format = None
        for path in word_dict.values():
            if file_format is None:
                file_format = path.suffix[1:]
            else:
                if str(file_format) != str(path.suffix[1:]):
                    log.error("Inconsistent audio formats in the word dict. File %s does not match expected format of %s", path, file_format)
                    raise InconsistentAudioFormats
        if not file_format:
            raise NoAudioFormatFound
        log.info("Audio format found: %s", file_format)
        return file_format

    def _get_words(self) -> List[str]:
        """Gets the available words for the voice

        Returns:
            List[str]: Words available to the voice
        """
        word_list = list(self._word_dict.keys())
        word_list.sort()
        return word_list

    def get_audio_format(self) -> str:
        """Get the audio format of the voice files as well as generated files
        Returns:
            (string): Audio format
        """
        return self._audio_format

    def _create_audio_segments(self, word_array: List[str]) -> List[AudioSegment]:
        words_audio: List[AudioSegment] = []
        for word in word_array:
            if word in PUNCTUATION_TIMING:
                words_audio.append(AudioSegment.silent(
                    PUNCTUATION_TIMING[word]))
            else:
                words_audio.append(AudioSegment.from_file(
                    self._word_dict[word], self._audio_format))
        return words_audio


class MultiVoice(Voice):
    """Voice class that uses other voices to assemble
    multi-voice sentences.

    Example: vox:hello hev:there
    Generates a sentence with one word from a voice
    called "vox" and another from a voice called "hev."
    """

    def __init__(self, voices: Dict[str, SingleVoice], database: Optional[DatabaseConnection]):
        """
        Args:
            voices (Dict[str, SingleVoice]): Voices to use to assemble sentences.
            database (Optional[DatabaseConnection]): Database connection information.
                If none provided, no database will be used and no data will persist.
        """
        super().__init__(name='multi', database=database)
        self._voices = voices

        self.words = self._get_words(voices)

    def _get_words(self, voices: Dict[str, SingleVoice]):
        words = []
        for name, voice in voices.items():
            voice_words = [f'{name}:{word}' for word in voice.words]
            words.extend(voice_words)
        return words

    def _get_word_and_voice_strings(self, words_and_voices: List[Tuple[str, SingleVoice]]) -> List[str]:
        """Turns array of word:voice assignments into string.

        Example: "vox:hello vox:there hev:doctor hev:freeman

        Args:
            words_and_voices (List[Tuple[str, SingleVoice]]): Word:voice assignments

        Returns:
            List[str]: Combined string
        """
        return [f'{voice.name}:{word}' for word, voice in words_and_voices]

    def _get_sentence_info(self, words: List[str]) -> Tuple[Sentence, List[str]]:
        # TODO: There is a good amount of double-processing going on here
        words_and_voices = self._get_word_voice_assignment(words)
        words_and_voices_strings = self._get_word_and_voice_strings(
            words_and_voices)
        sayable_words, unsayable_words = self.get_sayable_unsayable(
            words_and_voices_strings)
        sayable_sent_arr = [
            word_voice for word_voice in words_and_voices_strings if word_voice in sayable_words]
        combined_voice_sentences = self.get_combined_voice_sentences(
            words_and_voices)
        sentence_arr = []
        for voice, sentence_words in combined_voice_sentences:
            voice_sentence_segment = f'{voice.name}:{" ".join(sentence_words)}'
            sentence_arr.append(voice_sentence_segment)

        sayable_sent_str = ' '.join(sentence_arr)

        sentence = Sentence(
            sentence=sayable_sent_str,
            sayable=sayable_words,
            unsayable=unsayable_words,
            audio=None,
        )
        return sentence, sayable_sent_arr

    def get_sayable_unsayable(self, words: List[str]) -> Tuple[List[str], List[str]]:
        sayable = []
        unsayable = []
        words_and_voices = self._get_word_voice_assignment(words=words)
        combined_voice_sentences = self.get_combined_voice_sentences(
            words_and_voices)
        for voice, sentence_words in combined_voice_sentences:
            voice_sayable, voice_unsayable = voice.get_sayable_unsayable(sentence_words)
            voice_sayable = [f'{voice.name}:{word}' for word in voice_sayable]
            voice_unsayable = [
                f'{voice.name}:{word}' for word in voice_unsayable]
            sayable.extend(voice_sayable)
            unsayable.extend(voice_unsayable)
        sayable.sort()
        unsayable.sort()
        return sayable, unsayable

    def _create_audio_segments(self, word_array: List[str]) -> List[AudioSegment]:
        words_and_voices = self._get_word_voice_assignment(word_array)
        combined_voice_sentences = self.get_combined_voice_sentences(
            words_and_voices)
        return self.get_combined_audio(
            voice_sentences=combined_voice_sentences,
        )

    def _get_word_voice_assignment(self, words: List[str]) -> List[Tuple[str, SingleVoice]]:
        """Determines voice for each word in a list separated
        from a raw sentence. Only the first word must have a voice
        assignment, further assignments are inferred.

        Example: vox:hello there hev:doctor freeman
        The first two words are assigned to vox, second two to hev

        Args:
            words (List[str]): Words to determine voice assignment of

        Raises:
            FailedToSplit: Raised if unable to split a word/voice assignment.
            NoVoiceSpecified: Raised if initial voice cannot be determined.

        Returns:
            List[Tuple[str, SingleVoice]]: word:voice assignments
        """
        words_and_voices: List[Tuple[str, SingleVoice]] = []

        current_voice: Optional[SingleVoice] = None
        for word_maybe_voice in words:
            word_split = word_maybe_voice.split(':')
            word: Optional[str] = None
            voice: Optional[str] = None
            if len(word_split) == 1:
                word = word_split[0]
            elif len(word_split) == 2:
                voice = word_split[0]
                word = word_split[1]
            if not word:
                raise FailedToSplit

            if voice:
                current_voice = self._voices[voice]
            if not current_voice:
                raise NoVoiceSpecified
            word_and_voice = (word, current_voice)
            words_and_voices.append(word_and_voice)

        return words_and_voices

    def get_combined_voice_sentences(self, words_and_voices: List[Tuple[str, SingleVoice]]) -> List[Tuple[SingleVoice, List[str]]]:
        """Turns individual word:voice assignments into
        combined sentences for each word in sequence:

        Example: vox:hello vox: there hev:doctor hev:freeman vox:boop
        Returns vox:[hello, there] hev:[doctor freeman] vox:[boop]

        Args:
            words_and_voices (List[Tuple[str, SingleVoice]]): Word:voice assignments

        Returns:
            List[Tuple[SingleVoice, List[str]]]: Voice:sentence assignments
        """
        current_voice: Optional[SingleVoice] = None
        current_voice_sentence: List[str] = []
        voice_sentences: List[Tuple[SingleVoice, List[str]]] = []
        for word, voice in words_and_voices:
            if not current_voice:
                current_voice = voice
            if voice == current_voice:
                current_voice_sentence.append(word)
            else:
                voice_sentences.append((current_voice, current_voice_sentence))
                current_voice = voice
                current_voice_sentence = [word]
        if current_voice and current_voice_sentence:
            voice_sentences.append((current_voice, current_voice_sentence))
        return voice_sentences

    def get_combined_audio(self, voice_sentences: List[Tuple[SingleVoice, List[str]]]) -> List[AudioSegment]:
        """Generates audio segments for each voice sentence

        Args:
            voice_sentences (List[Tuple[SingleVoice, List[str]]]): Voice:sentence assignments

        Returns:
            List[AudioSegment]: List of generated audio segments
        """
        audio_segments = []
        for voice, words in voice_sentences:
            sentence = voice.generate_audio_from_array(
                words, save_to_db=False)
            if sentence.audio:
                audio_segments.append(sentence.audio)
        return audio_segments


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(
        description='Generate a sentence using a voice')
    parser.add_argument('-s', '--voice-dir', type=str, required=True,
                        help='Path to folder with voice audio files')
    parser.add_argument('-f', '--format', type=str, required=False,
                        default='wav', help='Audio format to export as')
    parser.add_argument('sentence', type=str)
    args = parser.parse_args()

    voice_dir = Path(args.voice_dir)
    if not voice_dir.is_dir():
        log.error('Voice dir at %s does not exist!', voice_dir)
        sys.exit(1)

    selected_voice = SingleVoice(name=voice_dir.name, path=voice_dir, database=None)
    generated_sentence = selected_voice.generate_audio(args.sentence)
    if generated_sentence is None or generated_sentence.audio is None:
        sys.exit(1)

    output_path = Path.cwd().joinpath(f"{generated_sentence.sentence}.{args.format}")

    generated_sentence.audio.export(output_path, format=args.format)
