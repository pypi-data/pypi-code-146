import os

from dataclasses import dataclass
from rich.prompt import (
    Confirm,
    IntPrompt,
    Prompt
)
from rich.table import Table
from typing import List

from fu.common.errors import MissingRequiredDataError
from fu.utils.console import console
from fu.utils.path import (
    get_file_name,
    get_file_ext,
    is_dir,
    path_files
)


_movie_formats = ['.mkv', '.mp4', '.avi', '.wmv']

@dataclass
class MovieFile:
    src_file: str

    title: str
    year: int
    resolution: str = None
    audio_lang: str = None
    extra_comment: str = None

    file_ext: str = None

    def make_file_name(self) -> str:
        """Creates file name for this movie using format:  \
            <Title> (<Year>) - [Resolution] [Audio language].<ext>

        Returns:
            str: File name for this movie
        """
        if not self.is_valid():
            raise MissingRequiredDataError()

        name = '{} ({})'.format(self.title, self.year)

        if self.resolution:
            name += ' - {}'.format(self.resolution)

        if self.audio_lang:
            name += '{} {}'.format(
                ('' if self.resolution else ' -'),
                self.audio_lang
            )

        if self.extra_comment:
            name += '{} {}'.format(
                ('' if self.resolution or self.audio_lang else ' -'),
                self.extra_comment
            )

        # Verify extension existence
        if self.file_ext:
            name += '{}'.format(self.file_ext)

        return name

    def make_target_file_path(self) -> str:
        """Creates destination file path for this movie

        Returns:
            str: Destination file path
        """
        if not self.is_valid():
            raise MissingRequiredDataError()

        file_name = self.make_file_name()
        dir_path = os.path.dirname(self.src_file)

        return os.path.join(dir_path, file_name)

    def is_valid(self) -> bool:
        return self.src_file \
                and os.path.isfile(self.src_file) \
                and self.title \
                and self.year


class RenameOrder:
    """Represents a rename movie files operation
    """

    def __init__(self, src_dir: str) -> None:
        """Initalizes order object

        Args:
            src_dir (str): Path to directory containing movies to \
                rename
        """
        self.src_dir = src_dir

        #: Movies that can be renamed without issue
        self.movies: List[MovieFile] = []

        #: Movies whose destination file already exists
        self.dst_existent_movies: List[MovieFile] = []

        #: File names of skipped movie files
        self.skipped_files: List[str] = []

        self.errors: List[str] = []
        self.warnings: List[str] = []

        #: Indicates if rename execution is approved by user
        self.execute = False

        #: Indicates if overwrite of destination files is approved
        self.overwrite = False

    def scan_src_dir(self) -> None:
        """Scans provided directory for movie files and ask user for  \
            movie info. \

            Scanned files will be stored into: movies, dst_existent_movies \
            and skipped_files lists.
        """
        console.print('Looking for movie files at: {}'.format(self.src_dir))

        for movie_file in path_files(self.src_dir, extensions=_movie_formats):
            src_file_name = get_file_name(movie_file)

            # Confirm rename request
            console.print('\n File found: {}'.format(src_file_name))
            rename_approved = Confirm.ask('Rename file?')

            if rename_approved:
                movie = self._ask_movie_details(movie_file)
                movie.file_ext = get_file_ext(movie_file)
                movie.src_file = movie_file

                # Wether destination file already exists
                if os.path.isfile(movie.make_target_file_path()):
                    self.dst_existent_movies.append(movie)

                # Movie can be renamed without issues
                else:
                    self.movies.append(movie)

            # Skipped file
            else:
                self.skipped_files.append(src_file_name)

    def evaluate_rename_order(self) -> None:
        """Shows rename order to user (including warnings/errors)    \
            and ask for confirmation to proceed and execute rename   \
            operations.

            If order has errors, it will be printed and execution    \
            will be set to false.
        """
        if self.has_errors():
            for error in self.errors:
                console.print(error, style='error')
            self.execute = False
            return None

        self._print_preview()

        if self.has_warnings():
            for warn in self.warnings:
                console.print(warn, style='warning')

            console.print()
            console.print('0. Abort operation')
            console.print('1. Rename only safe files')
            console.print('2. Rename all and overwrite existent files')
            user_choice = Prompt.ask(
                'Enter your choice: ',
                choices=['0', '1', '2'],
                default='1'
            )

            if user_choice == 0:
                self.execute = False
            elif user_choice == 1:
                self.overwrite = False
                self.execute = True
            elif user_choice == 2:
                self.overwrite = True
                self.execute = True

        # Confirm operation execution
        else:
            self.execute = Confirm.ask('Confirm rename operation?')

    def apply(self) -> None:
        """Applies rename operations based on user preferences
        """
        if not self.execute:
            return None

        for movie in self.movies:
            os.replace(
                movie.src_file,
                movie.make_target_file_path()
            )

        if self.dst_existent_movies and self.overwrite:
            for movie in self.dst_existent_movies:
                os.replace(
                    movie.src_file,
                    movie.make_target_file_path()
                )

        console.print()
        console.print('Rename operation is complete')

    def _ask_movie_details(self, src_file: str) -> MovieFile:
        title = Prompt.ask('Movie title: ')
        year = IntPrompt.ask('Year: ')
        movie = MovieFile(
            title=title,
            year=year,
            src_file=src_file
        )

        movie.resolution = Prompt.ask(
            '[Resolution (eg: 720p|1080p|4k)]: ',
            default=''
        )
        movie.audio_lang = Prompt.ask(
            '[Language (eg: Eng|Lat|Dual)]: ',
            default=''
        )
        movie.extra = Prompt.ask(
            '[Extra data (eg: HDR|Extended|3D)]: ',
            default=''
        )

        return movie

    def _print_preview(self) -> None:
        """Prints a table with details about this rename order
        """
        table = Table()
        table.add_column('Current file name', justify='right')
        table.add_column('New file name', justify='left')
        table.add_column('Status', justify='center')

        for movie in self.movies:
            table.add_row(
                get_file_name(movie.src_file),
                movie.make_file_name(),
                'Ok'
            )

        for movie in self.dst_existent_movies:
            table.add_row(
                '[yellow]{}'.format(get_file_name(movie.src_file)),
                '[yellow]{}'.format(movie.make_file_name()),
                '[yellow]Existent'
            )

        console.print()
        console.print(table)

    def has_errors(self) -> bool:
        if not self.movies and not self.dst_existent_movies:
            self.errors.append('No files to rename')

        return len(self.errors) > 0

    def has_warnings(self) -> bool:
        if self.dst_existent_movies:
            self.warnings.append('Some movie files will be overwriten')

        return len(self.warnings) > 0


def rename_movies(src_dir: str) -> None:
    """Will rename all movie files in provided directory asking user \
        for title, year, res, audio lang and extra comment

    Args:
        src_dir (str): Path to directory containing files to rename
    """
    if not is_dir(src_dir):
        console.print(
            'Provided dir does not exists. {}'.format(src_dir),
            style='error'
        )

    rename_order = RenameOrder(src_dir)
    rename_order.scan_src_dir()
    rename_order.evaluate_rename_order()

    if rename_order.execute:
        rename_order.apply()
