import rich
import warnings
from itertools import cycle

from typing import Any, Callable, List, Dict, Iterable
from rich.console import Console
from rich.progress import (
    Progress, BarColumn, TextColumn,
    TimeRemainingColumn, TimeElapsedColumn,
    SpinnerColumn
)

from iotree.utils.paths import (
    package_dir, base_dir, config_dir, safe_config_load
)

symbols, themes, user_infos, local_config = safe_config_load()


def call_any(funcs: List[Callable], *args, **kwargs) -> Any:
    """Try all functions in a list until one succeeds."""
    for f in funcs:
        try:
            return f(*args, **kwargs)
        except Exception as e:
            continue
    if "msg" in kwargs:
        raise ValueError(f'All functions failed. {kwargs["msg"]}')
    else:
        msg = [
            f"\n - {funcs[0].__name__} failed with args: {args} and kwargs: {kwargs}" for f in funcs
        ]
        msg = "f'All functions failed:" + "".join(msg)
        raise ValueError(msg)
    

def format_user_theme(theme: Dict[str,str]) -> Dict[str,str]:
    """Format a user theme to be used by rich."""
    must_have = [
        "description", "complete",
        "finished", "remaining",
        "message"]
    
    default = {
        "description": "bold purple",
        "complete": "bold green3",
        "finished": "bold green3",
        "remaining": "bold pink3",
        "message": "magenta",
        "spinner": "dots",
        "bar_width": 70,
    }
    
    for mh in must_have:
        if mh in theme:
            default[mh] = theme[mh]
        for k, v in theme.items():
            if k.endswith(mh):
                default[k] = v
    return default

def apply_progress_theme(
    theme: Dict[str, str],
    console: Console = None,
    ) -> Progress:
    """Apply a theme to the progress bar."""
    theme = format_user_theme(theme)
    
    return Progress(
                SpinnerColumn(theme["spinner"]),
                TextColumn("{task.description}", justify="right", style=theme.get("task.description", theme["description"])),
                BarColumn(bar_width=None),
                "[progress.percentage]{task.percentage:>3.1f}%",
                TimeElapsedColumn(),
                TimeRemainingColumn(),
                console=console,
            )
    

def basic_pbar(
    console: Console = None,
    ) -> Progress:
    return apply_progress_theme(theme=format_user_theme({}), console=console)

def rich_func(func, *args, **kwargs) -> Any:
    """Run a function with rich progress bar."""
    args = [], kwargs = {}
    theme = kwargs.pop("theme") if "theme" in kwargs else format_user_theme({})
    console = kwargs.pop("console") if "console" in kwargs else Console()
    pbar = kwargs.pop("progress") if "progress" in kwargs else apply_progress_theme(theme=theme, console=console)
    with pbar:
        task_id = pbar.add_task(f"Running {func.__name__}", total=None)
        try:
            result = func(*args, **kwargs)
            pbar.update(task_id, advance=100)
        except Exception as e:
            pbar.console.print(f"[bold red]Error while running {func.__name__}[/bold red]")
            pbar.console.print(e)
            pbar.update(task_id, advance=100)
            raise e
    return result
    
        
    
def rich_func_chainer(
    funcs: List[Callable], params: List[Any], *args, **kwargs
    ) -> Iterable[Any]:
    """Run a list of functions with rich progress bar.
    
    If you want to customize the progress bar, you can pass a `progress` keyword argument.
    If you want to customize the console, you can pass a `console` keyword argument.
    If you want a specific color theme or style for the progress bar, you can pass a `theme` keyword argument.
    
    Args:
        funcs (List[Callable]): A list of functions to run.
        params (List[Any]): A list of parameters to pass to each function. They must be in the same order as the functions.
        *args: Arguments to pass to each function. These will be passed to all functions.
        **kwargs: Keyword arguments to pass to each function. These will be passed to all functions.

    Returns:
        Iterable[Any]: An iterable of the results of each function.
    """
    if not isinstance(funcs, Iterable):
        funcs = [funcs]
    if len(funcs) < len(params):
            funcs = funcs*len(params) if len(funcs) == 1 else cycle(funcs)
    else:
        warnings.WarningMessage("The number of functions must be < than number of parameters or must be the same.", "Incorrect Value", __file__, 0)
    
    progress = kwargs.pop("progress", None)
    console = kwargs.pop("console", None)
    theme = kwargs.pop("theme", None)
    
    if console is None:
        console = Console()
    if progress is None:
        if theme is None:
            progress = Progress(
                SpinnerColumn(),
                TextColumn("[bold purple]{task.description}", justify="right"),
                BarColumn(bar_width=None),
                "[progress.percentage]{task.percentage:>3.1f}%",
                TimeElapsedColumn(),
                TimeRemainingColumn(),
                console=console,
            )

        else:
            progress = apply_progress_theme(theme=theme, console=console)

    errs = []

    with progress:
        for i, f in enumerate(funcs):
            task_id = progress.add_task(f"Running {f.__name__}", total=1)
            try:
                if isinstance(params[i], list):
                    result = f(*params[i], *args, **kwargs)
                elif isinstance(params[i], dict):
                    result = f(*args, **params[i], **kwargs)
                else:
                    result = f(params[i], *args, **kwargs)

                progress.update(task_id, advance=1)
            except Exception as e:
                progress.console.print(f"[bold red]Error while running {f.__name__}[/bold red]")
                progress.console.print(e)
                progress.update(task_id, advance=1)
                errs.append(e)
                result = None
            yield i, result
    if errs:
        fmt_errs = '\n - '.join([str(e) for e in errs])
        raise ValueError(f"Errors while running functions: {fmt_errs}")