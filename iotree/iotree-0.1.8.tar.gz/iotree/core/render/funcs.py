import rich

from typing import Any, Callable, List, Dict
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
    
        
        
    
    
def rich_func_chainer(
    funcs: List[Callable], *args, **kwargs
    ) -> Any:
    """Run a list of functions with rich progress bar.
    
    If you want to customize the progress bar, you can pass a `progress` keyword argument.
    If you want to customize the console, you can pass a `console` keyword argument.
    If you want a specific color theme or style for the progress bar, you can pass a `theme` keyword argument.
    
    Args:
        funcs (List[Callable]): A list of functions to run.
        *args: Arguments to pass to each function.
        **kwargs: Keyword arguments to pass to each function.
    """
    
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