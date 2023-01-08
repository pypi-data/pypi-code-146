"""Manages multiple voices
"""
import argparse
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union

import sqlalchemy

from hlvox.voice import MultiVoice, SingleVoice, Voice

log = logging.getLogger(__name__)


class DuplicateVoice(Exception):
    """Raised when duplicate voices are found
    """


@dataclass
class RemoteDatabaseInfo:
    """Database connection information if using remote database (sql)
    """
    name: str
    url: str
    port: int
    username: str
    password: str


@dataclass
class LocalDatabaseInfo:
    """Database info if using local file-based database (sqlite)
    """
    base_path: Path


class Manager:
    """Manages multiple voices
    """

    def __init__(
        self,
        voices_path: Union[Path, str],
        database_info: Optional[Union[LocalDatabaseInfo, RemoteDatabaseInfo]]
    ):
        self.voices_path = Path(voices_path)
        self._database_info = database_info

        # This strangeness is to make mypy happy. There is probably a cleaner way to do it.
        single_voices = self._load_voices(self.voices_path)
        multi_voice = self._create_multi_voice(single_voices)
        voices: Dict[str, Union[MultiVoice, SingleVoice]] = {}
        voices.update(single_voices)
        voices['multi'] = multi_voice
        self.voices = voices

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.exit()

    def _create_db_path(self, databases_path: Path, voice_name: str) -> Path:
        db_path = databases_path / voice_name
        db_path.mkdir(parents=True, exist_ok=True)
        return db_path

    def _create_db(self, database_info: Union[LocalDatabaseInfo, RemoteDatabaseInfo], voice_name: str) -> sqlalchemy.engine.Engine:
        dbi = database_info
        if isinstance(dbi, LocalDatabaseInfo):
            path = self._create_db_path(databases_path=dbi.base_path, voice_name=voice_name)
            return sqlalchemy.create_engine(f'sqlite:///{path}/db.sqlite')
        return sqlalchemy.create_engine(f'postgresql+psycopg2://{dbi.username}:{dbi.password}@{dbi.url}:{dbi.port}/{dbi.name}', pool_pre_ping=True)

    def _load_voices(self, path: Path) -> Dict[str, SingleVoice]:
        voices = {}
        voice_folders = list(x for x in path.iterdir() if x.is_dir())
        for voice_folder in voice_folders:
            voice_name = voice_folder.name.lower()
            if voice_name in voices:
                raise DuplicateVoice('Duplicate voice name found')

            database = None
            if self._database_info is not None:
                database = self._create_db(database_info=self._database_info, voice_name=voice_name)
            new_voice = SingleVoice(
                name=voice_name, path=voice_folder, database=database)
            voices[new_voice.name] = new_voice
        return voices

    def _create_multi_voice(self, voices: Dict[str, SingleVoice]) -> MultiVoice:
        database = None
        if self._database_info is not None:
            database = self._create_db(database_info=self._database_info, voice_name='multi')
        return MultiVoice(
            voices=voices,
            database=database,
        )

    def get_voice_names(self) -> List[str]:
        """Gets names of available voices

        Returns:
            list -- list of voice name strings
        """

        voice_names = list(self.voices.keys())
        voice_names.sort()
        return voice_names

    def get_voice(self, name: str) -> Optional[Voice]:
        """Get voice of requested name

        Args:
            name ({string}): name of voice to get

        Returns:
            {voxvoice}: requested voice
        """
        if name in self.voices:
            return self.voices[name]
        return None

    def exit(self):
        """Exit all loaded voices
        """
        for voice in self.voices.values():
            voice.exit()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(
        description='Generate a sentence using voices')
    parser.add_argument('-s', '--voices-dir', type=str, required=True,
                        help='Path to folder with voice audio file folders')
    parser.add_argument('-f', '--format', type=str, required=False,
                        default='wav', help='Audio format to export as')
    parser.add_argument('voice', type=str)
    parser.add_argument('sentence', type=str)
    args = parser.parse_args()

    voices_dir = Path(args.voices_dir)
    if not voices_dir.is_dir():
        log.error('Voices dir at %s does not exist!', voices_dir)
        sys.exit(1)

    manager = Manager(
        voices_path=voices_dir,
        database_info=None,
    )

    loaded_voice = manager.get_voice(args.voice)
    if loaded_voice is None:
        log.error("Voice %s was not found", loaded_voice)
        sys.exit(1)

    sentence = loaded_voice.generate_audio(args.sentence)
    if sentence is None or sentence.audio is None:
        log.error('Cannot generate %s: %s', sentence.sentence, sentence)
        sys.exit(1)

    # Paths can't have : in them, so replace with % as a stand-in
    sanitized_sentence = sentence.sentence.replace(':', '%')
    output_path = Path.cwd().joinpath(f"{sanitized_sentence}.{args.format}")

    log.info('Exporting to %s', output_path)
    sentence.audio.export(output_path, format=args.format)
