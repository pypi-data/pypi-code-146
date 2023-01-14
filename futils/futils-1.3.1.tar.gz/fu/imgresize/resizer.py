import os

from PIL import Image
from pathlib import Path
from resizeimage import resizeimage
from rich.table import Table
from rich.prompt import Prompt
from dataclasses import (
    dataclass,
    field
)

from fu.utils.console import console
from fu.utils.path import (
    get_file_name,
    is_dir,
    path_files
)


_img_formats = ['.png', '.jpg', '.jpeg']
_MIN_WIDTH = 320
_MIN_HEIGHT = 480

@dataclass
class ResizeOrder:
    """A Wrapper for results of resize preview operations

    Args:
        src_dir (str): uri to directory where images to resize   \
            are located
        tgt_width (int): Desired width in pixels
        tgt_height (int): Desired height in pixels
        dst_dir (str): Path to destination directory where       \
            resized image are going to be saved
        gral_errors (list[str]): General errors, resize will not \
            be possible
        invalid_images (list[str]): uri of images that can't be  \
            resized, most likely cause it has smaller size than  \
            desired output
        existent_images (list[ResizedImg]): Images that already  \
            exists in target directory
        ok_images (list[ResizedImg]): Images that can be resized \
            without issues
        execute (bool): Indicates if order was approved by user  \
            for execution
        overwrite (bool): Indicate if user request overwrite     \
            already existent images
    """

    src_dir: str
    tgt_width: int
    tgt_height: int

    dst_dir: str = None
    gral_errors: list = field(default_factory=list)

    invalid_images: list = field(default_factory=list)
    existent_images: list = field(default_factory=list)
    ok_images: list = field(default_factory=list)

    execute: bool = False
    overwrite: bool = False

    def has_warnings(self) -> bool:
        return self.existent_images or self.invalid_images


@dataclass
class ResizedImg:
    src_file: str
    dst_file: str


class TargetSizeError(Exception):
    pass


class TargetDirNotFoundError(Exception):
    pass


def resize_images(
        src_dir: str,
        tgt_width: int,
        tgt_height: int,
        dst_dir: str = None
    ) -> None:

    resize_order = ResizeOrder(src_dir, tgt_width, tgt_height, dst_dir)
    _evaluate_resize_order(_preview_resize(resize_order))

    if not resize_order.execute:
        return None

    if not resize_order.dst_dir:
        resize_order.dst_dir = _make_destination_dir_uri(
            resize_order.src_dir,
            resize_order.tgt_width,
            resize_order.tgt_height
        )

    if not is_dir(resize_order.dst_dir):
        Path(resize_order.dst_dir).mkdir(parents=True, exist_ok=True)
        
        # Verify directory was created
        if not is_dir(resize_order.dst_dir):
            raise TargetDirNotFoundError()

    for resize_img in resize_order.ok_images:
        resize_img.dst_file = _resize(
            resize_img.src_file,
            resize_order.tgt_width,
            resize_order.tgt_height,
            resize_order.dst_dir
        )

    if resize_order.overwrite:
        for resize_img in resize_order.existent_images:
            resize_img.dst_file = _resize(
                resize_img.src_file,
                resize_order.tgt_width,
                resize_order.tgt_height,
                resize_order.dst_dir
            )
        

def _resize(src_file: str, tgt_width: int, tgt_height: int, dst_dir: str):
    """Resizes provided image file into indicated width    \
    and height and stores resulting images into dst_dir

    Args:
        src_file (str): Path to source file image
        tgt_width (int): Desired width in pixels
        tgt_height (int): Desired height in pixels
        dst_dir (str): Path to destination directory where \
            resized image is going to be saved

    Returns:
        str: Path to resized image file
    """
    if tgt_width < _MIN_WIDTH or tgt_height < _MIN_HEIGHT:
        raise TargetSizeError()

    dst_file = ''
    with Image.open(src_file) as img:
        resized_img = resizeimage.resize_cover(
            img,
            [tgt_width, tgt_height]
        )

        dst_file = _make_destination_uri(
            src_file,
            dst_dir,
            tgt_width,
            tgt_height
        )
        
        resized_img.save(dst_file, img.format)
    
    return dst_file


def _preview_resize(resize_order: ResizeOrder) -> ResizeOrder:
    """Verify if resize operation will be possible with provided
    parameters. Resize operations will NOT be done by this method.

    Args:
        resize_order (ResizeOrder): Resize order with tgt_width \
            and tgt_height assigned
    Returns
        ResizeOrder: Resize order with images and errors updated
    """

    if resize_order.tgt_width < _MIN_WIDTH:
        resize_order.gral_errors.append('Minimal supported width is {}px'.format(
            _MIN_WIDTH
        ))

    if resize_order.tgt_height < _MIN_HEIGHT:
        resize_order.gral_errors.append('Minimal supported height is {}px'.format(
            _MIN_HEIGHT
        ))
    
    if resize_order.gral_errors:
        return resize_order

    if not resize_order.dst_dir:
        resize_order.dst_dir = _make_destination_dir_uri(
            resize_order.src_dir,
            resize_order.tgt_width,
            resize_order.tgt_height
        )

    # Validate each image
    for img_file in path_files(resize_order.src_dir, _img_formats):
        with Image.open(img_file) as img:
            img_w, img_h = img.size
            
            if img_w < resize_order.tgt_width:
                resize_order.invalid_images.append(ResizedImg(
                    src_file=img_file,
                    dst_file=None
                ))
                continue
            
            if img_h < resize_order.tgt_height:
                resize_order.invalid_images.append(ResizedImg(
                    src_file=img_file,
                    dst_file=None
                ))
                continue

            destination = _make_destination_uri(
                img_file,
                resize_order.dst_dir,
                resize_order.tgt_width,
                resize_order.tgt_height
            )
            if Path(destination).exists():
                resize_order.existent_images.append(ResizedImg(
                    src_file=img_file,
                    dst_file=destination
                ))

            else:
                resize_order.ok_images.append(ResizedImg(
                    src_file=img_file,
                    dst_file=destination
                ))

    # Verify there are images to resize
    if not resize_order.ok_images and not resize_order.existent_images:
        resize_order.gral_errors.append(
            'No valid images were found at {}'.format(resize_order.src_dir)
        )

    return resize_order


def _evaluate_resize_order(order: ResizeOrder, verbose=False) -> ResizeOrder:
    """Evaluates resize order (After preview operation) and shows
    errors or warnings to user. If there are warnings, will ask
    user if should proceed or abort resize operation

    Args:
        order (PreviewResult): Resize preview result
        verbose (bool): If true, will print a detailed table of every \
            found image. Default: False

    Returns:
        ResizeOrder: Updated object indicating if resize should
        proceed or not
    """
    
    if order.gral_errors:
        for error in order.gral_errors:
            console.print(error, style='error')

        order.execute = False
        return order

    if not order.has_warnings():
        order.execute = True
        return order

    if verbose:
        table = Table()
        table.add_column('Image file', justify='right')
        table.add_column('Status')

        for img in order.ok_images:
            table.add_row(get_file_name(img.src_file), '[green]Ok')

        for img in order.existent_images:
            table.add_row(get_file_name(img.src_file), '[yellow]Existent')

        for img in order.invalid_images:
            table.add_row(get_file_name(img.src_file), '[red]Too small')
        
        console.print()
        console.print(table)

    # Print summary
    console.print('\nResize summary:')
    if order.ok_images:
        console.print(
            ' {} {} can be resized without issues'.format(
                len(order.ok_images),
                ('Images' if len(order.ok_images) > 1 else 'Image')
            ),
            style='success'
        )
    if order.existent_images:
        console.print(
            ' {} {} will override destination {}'.format(
                len(order.existent_images),
                ('Images' if len(order.existent_images ) > 1 else 'Image'),
                ('files' if len(order.existent_images) > 1 else 'file')
            ),
            style='warning'
        )
    if order.invalid_images:
        console.print(
            ' {} {} will not be resized'.format(
                len(order.invalid_images),
                ('Images' if len(order.invalid_images ) > 1 else 'Image')
            ),
            style='error'
        )
        
    # Ask for confirmation
    user_choice = ''
    console.print('\nEnter your choice')
    console.print(' 0. Abort')
    console.print(' 1. View details')

    if order.existent_images:
        if order.ok_images:
            console.print(' 2. Resize all images (Overwrite existent)')
            console.print(' 3. Resize only safe images (Don\'t overwrite)')
            user_choice = Prompt.ask(
                'Your choice',
                choices=['0', '1', '2', '3'],
                default='3'
            )

            if user_choice == '3':
                order.overwrite = False
                order.execute = True

        # All images are existent or invalid
        else:
            console.print(' 2. Resize valid images (Overwrite existent)')
            user_choice = Prompt.ask(
                'Your choice',
                choices=['0', '1', '2'],
                default='2'
            )

        if user_choice == '2':
            order.overwrite = True
            order.execute = True

    # All images are valid or invalid (No existent images)
    else:
        console.print(' 2. Resize all valid images')
        user_choice = Prompt.ask(
            'Your choice',
            choices=['0', '1', '2'],
            default='2'
        )

        if user_choice == '2':
            order.execute = True    

    if user_choice == '0':
        console.print('\nAborting resize', style='info')
        order.execute = False
    elif user_choice == '1':
        return _evaluate_resize_order(order, verbose=True)

    return order


def _make_destination_uri(src_file: str, dst_dir: str,
                          width: int, height: int):
    """Creates destination uri for provided image file

    Args:
        src_file (str): Path to source image file
        dst_dir (str): Destination directory path
        width (int): Width in pixels
        height (int): Height in pixels
    """
    filename = get_file_name(src_file, include_extension=False)
    file_ext = Path(src_file).suffix

    dst_file_name = '{}_{}x{}{}'.format(
        filename,
        width,
        height,
        file_ext
    )

    return os.path.join(
        dst_dir,
        dst_file_name
    )


def _make_destination_dir_uri(source_dir: str, width: int, height: int):
    """Creates destination directory uri

    Args:
        source_dir (str): Path to source directory
        width (int): Width in pixels
        height (int): Height in pixels
    """
    dir_name = '{}x{}'.format(width, height)
    return os.path.join(source_dir, dir_name)
