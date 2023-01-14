import typer

from fu.imgresize.resizer import resize_images
from fu.index import idx_svc
from fu.iterate_files import iterate_and_open, iterate_from_file
from fu.movie.fixname import rename_movies
from fu.tvshow.fixname import rename_tvshow_files

from fu.exif import exif_app


app = typer.Typer()
app.add_typer(exif_app.app, name='exif')


@app.command()
def imgresize(
    src_dir: str = typer.Argument(
        "./",
        help="Directory containing images to resize"
    ),
    tgt_width: int = typer.Option(
        1920,
        "--width",
        "-w",
        help="Desired width in pixels"
    ),
    tgt_height: int = typer.Option(
        1080,
        "--height",
        "-h",
        help="Desired height in pixels"
    ),
    dst_dir: str = typer.Option(
        None,
        "--dst-dir",
        "-d",
        help="Destination directory for resized images"
    )
):
    """Resize images to smaller resolution applying same effect
    as css 'cover'
    """
    resize_images(src_dir, tgt_width, tgt_height, dst_dir)


@app.command()
def moviefixname(src_dir: str = typer.Argument(
    "./",
    help="Directory containing movie files to rename"
)):
    """Renames movie files to make them scanners friendly
    """
    rename_movies(src_dir)

@app.command()
def tvshowfixnames(
    src_dir: str = typer.Argument(
        "./",
        help="Directory containing tv show files to rename"
    )
):
    """Renames TV Show files to make them scanners friendly
    """
    rename_tvshow_files(src_dir)


@app.command()
def iterate(
    path: str = typer.Argument(
        "./",
        help="Directory containing files to iterate over"
    ),
    step: int = typer.Option(
        1,
        "--step",
        "-s",
        help="Number of files to open at a time"
    )
):
    """Iterates all files in given path and opens them
    in default system application
    """
    iterate_and_open(path, step)

@app.command()
def iteratefrom(
    path: str = typer.Argument(
        ...,
        help='Path to file containing the paths to iterate'
    ),
    step: int = typer.Option(
        1,
        '--step',
        '-s',
        help='Number of files to open at a time'
    )
):
    """Will iterate each line of given file as a path
    and will open it in default system program.

    Empty lines or lines starting with '#' will be
    ignored.
    """
    iterate_from_file(path, step)

@app.command()
def index(
    path: str = typer.Argument(
        ...,
        help='Directory to index'
    ),
    output: str = typer.Option(
        None,
        '--output',
        '-o',
        help=(
            'Name for generated index file. '
            'Defaults to "idx-<date>-<time>-<microseconds>.txt"'
        )
    )
):
    """Creates a text file listing all files at given path
        in ascending order. Only direct children files.
    """
    idx_svc.index_dir(path, output)


@app.command('index-removed')
def index_removed(
    idx: str = typer.Argument(
        ...,
        help='Index of files to verify in specified path'
    ),
    path: str = typer.Argument(
        ...,
        help='Where to look for files in index'
    ),
    output: str = typer.Option(
        None,
        '--output',
        '-o',
        help=(
            'Name for generated index file of not found '
            'items. Defaults to "idx-removed-<date>-<time>-<microseconds>.txt"'
        )
    )
):
    """Creates a text file listing all files that are present in a given
        index but doesn't exists in specified path anymore.
    """
    idx_svc.index_deleted_from(path, idx, output)


if __name__ == "__main__":
    app()