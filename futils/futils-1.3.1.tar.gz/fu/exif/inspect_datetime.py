import os
import typer
from exif import Image
from rich.prompt import Confirm
from rich.table import Table
from fu.common.errors import InvalidPathError
from fu.utils.path import path_files
from fu.utils.console import console


_IMG_EXTENSIONS = ['.jpg', '.jpeg']

class ExifImage:
    def __init__(self, img: Image) -> None:
        self.img = img
        self.has_exif = img.has_exif

    def has_datetime(self):
        return self.has_exif and hasattr(self.img, 'datetime')

    def has_datetime_digitized(self):
        return self.has_exif and hasattr(self.img, 'datetime_digitized')

    def has_datetime_original(self):
        return self.has_exif and hasattr(self.img, 'datetime_original')

    @property
    def datetime(self):
        """Time when the file was created. \
            \
            In a digital camera, usually is the same time the image \
            was taken.\
            \
            If the image was edited, this could be the time the new \
            file (edited version) was created.

        Returns:
            datetime: Date and time of file creation
        """
        if self.has_datetime():
            return self.img.datetime
        return None

    @property
    def datetime_original(self):
        """Time when the image was taken

        Returns:
            datetime: Date and time when image was captured
        """
        if self.has_datetime_original():
            return self.img.datetime_original
        return None

    @property
    def datetime_digitized(self):
        """Time when image was digitalized, e.g. the moment it was scanned

        Returns:
            datetime: Date and time when image was digitalized
        """
        if self.has_datetime_digitized():
            return self.img.datetime_digitized
        return None


def inspect_dir(path: str, step: int = 100) -> None:
    """Will inspect exif metadata for each image file \
        at given directory and will print a table with \
        found metadata

    Args:
        path (str): Directory containing images to inspect
        step (int, optional): How many files inspect at a time. \
            Defaults to 1.
    """
    meta_table = _empty_exif_table()

    for img_path in path_files(path, _IMG_EXTENSIONS):
        with open(img_path, 'rb') as r_img:
            img = ExifImage(Image(r_img))

            meta_table.add_row(
                os.path.basename(img_path),
                img.datetime,
                img.datetime_original,
                img.datetime_digitized)

    console.print(meta_table)


def inspect_from_file(filepath: str, step=1, display_img=False) -> None:
    """Inspect metadata for every file path provided at given \
        file. Each line of file (non empty and not starting with '#') \
        will be read as a file path.

    Args:
        filepath (str): Path to file with paths to inspect.
        step (int): Indicates how many images (lines) inspect at a time.
        display_img (bool, optional): If images should be open in default \
            system viewer. Defaults to False.
    """
    if not os.path.isfile(filepath):
        console.print(
            f'Path is not a valid file: { filepath }',
            style='error')
        raise InvalidPathError()

    meta_table = _empty_exif_table()

    with open(filepath) as pathsfile:
        curr_open_count = 0

        for filepath in pathsfile:
            filepath = filepath.strip("\n")

            if filepath and not filepath.startswith('#'):

                # Read exif metadata
                with open(filepath, 'rb') as raw_img:
                    img = ExifImage(Image(raw_img))

                    meta_table.add_row(
                        os.path.basename(filepath),
                        img.datetime,
                        img.datetime_original,
                        img.datetime_digitized)

                # Open image in system viewer if required by user
                if display_img:
                    typer.launch(filepath)

                curr_open_count += 1

                # Pause opening files if step has been reached
                if curr_open_count == step:
                    console.print(meta_table)
                    meta_table = _empty_exif_table()

                    curr_open_count = 0
                    if not Confirm.ask('Open next {} file(s)'.format(step)):
                        break

        if curr_open_count > 0:
            console.print(meta_table)

def _empty_exif_table() -> Table:
    meta_table = Table()
    meta_table.add_column('Filename')
    meta_table.add_column('File creation time')
    meta_table.add_column('Original datetime')
    meta_table.add_column('Digitalized datetime')

    return meta_table
