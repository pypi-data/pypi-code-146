import os
import urllib.request
import click
from tqdm import tqdm
from pathlib import Path


def __add_header(snake_installer):
    def inner(f):
        """
        replace_package_name on help.
        param f: function to decorate
        return: decorated function
        """
        click.secho(f"{snake_installer.description_tool}{snake_installer.get_last_version()}", fg='green')
        return f
    return inner


def __replace_package_name(snake_installer):
    def inner(f):
        """
        replace_package_name on help.
        param f: function to decorate
        return: decorated function
        """
        f.__doc__ = f"{f.__doc__.strip().replace('tool', snake_installer.soft_name).rstrip()}"
        return f
    return inner


def check_privileges():
    """used to know if user have root access to reset package installation"""
    if not os.environ.get("SUDO_UID") and os.geteuid() != 0:
        click.secho(f"\n    ERROR : You need to run -r, --restore with sudo privileges or as root\n", fg="red")
    else:
        return True


class DownloadProgressBar(tqdm):
    """Build progress bar on terminal for downloading url link"""

    def __init__(self, *args, **kargs):
        self.total = None
        super().__init__(*args, **kargs)

    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(tuple_value):
    """download url to output path"""
    url, output_path = tuple_value
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


def multiprocessing_download(urls_list, threads=2):
    """Used multiprocessing for download URL list on parallel"""
    from multiprocessing.pool import ThreadPool
    return ThreadPool(threads).imap_unordered(download_url, urls_list)


def __command_required_option_from_option(require_name, require_map):
    import click

    class CommandOptionRequiredClass(click.Command):
        def invoke(self, ctx):
            require = ctx.params[require_name]
            if require not in require_map:
                raise click.ClickException(click.style(f"Unexpected value for --'{require_name}': {require}\n", fg="red"))
            if ctx.params[require_map[require].lower()] is None:
                raise click.ClickException(click.style(f"With {require_name}={require} must specify option --{require_map[require]} path/to/modules\n", fg="red"))
            super(CommandOptionRequiredClass, self).invoke(ctx)
    return CommandOptionRequiredClass


def get_dir(path):
    """List of directory included on folder"""
    return [elm.name for elm in Path(path).glob("*") if elm.is_dir()]


def get_files_ext(path, extensions, add_ext=True):
    """List of files with specify extension included on folder

    Arguments:
        path (str): a path to folder
        extensions (list or tuple): a list or tuple of extension like (".py")
        add_ext (bool): if True (default), file have extension

    Returns:
        :class:`list`: List of files name with or without extension , with specify extension include on folder
        :class:`list`: List of  all extension found

     """
    if not (extensions, (list, tuple)) or not extensions:
        raise ValueError(f'ERROR: "extensions" must be a list or tuple not "{type(extensions)}"')
    tmp_all_files = []
    all_files = []
    files_ext = []
    for ext in extensions:
        tmp_all_files.extend(Path(path).glob(f"**/*{ext}"))

    for elm in tmp_all_files:
        ext = "".join(elm.suffixes)
        if ext not in files_ext:
            files_ext.append(ext)
        if add_ext:
            all_files.append(elm.as_posix())
        else:
            if len(elm.suffixes) > 1:

                all_files.append(Path(elm.stem).stem)
            else:
                all_files.append(elm.stem)
    return all_files, files_ext


def var_2_bool(key, tool, to_convert):
    """convert to boolean"""
    if isinstance(type(to_convert), bool):
        return to_convert
    elif f"{to_convert}".lower() in ("yes", "true", "t"):
        return True
    elif f"{to_convert}".lower() in ("no", "false", "f"):
        return False
    else:
        raise TypeError(
            f'CONFIG FILE CHECKING FAIL : in the "{key}" section, "{tool}" key: "{to_convert}" is not a valid boolean')


def convert_genome_size(size):
    import re
    mult = dict(K=10 ** 3, M=10 ** 6, G=10 ** 9, T=10 ** 12, N=1)
    search = re.search(r'^(\d+\.?\d*)\s*(.*)$', size)
    if not search or len(search.groups()) != 2:
        raise ValueError(
            f"CONFIG FILE CHECKING FAIL : not able to convert genome size please only use int value with{' '.join(mult.keys())} upper or lower, N or empty is bp size")
    else:
        value, unit = search.groups()
        if not unit:
            return int(value)
        elif unit and unit.upper() not in mult.keys():
            raise ValueError(
                f"CONFIG FILE CHECKING FAIL : '{unit}' unit value not allow or not able to convert genome size please only use int value with{' '.join(mult.keys())} upper or lower, N or empty is bp size")
        else:
            return int(float(value) * mult[unit.upper()])
