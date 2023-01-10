import rich
from time import sleep

from rich.tree import Tree
from rich.color import Color
from rich.panel import Panel
from typing import Any, Dict, List, Union, Optional, Tuple

from iotree.core.render.trees import build
from iotree.utils.paths import (
    package_dir, base_dir, config_dir, safe_config_load
)

symbols, themes, user_infos, local_config = safe_config_load()

##########################################
############ DEMO UTILS ##################
##########################################

def print_demo(symbol: str, exlist: List[str]) -> None:
    """Print a demo of a symbol."""
    rich.print(f"If you use the [bold yellow]{symbol}[/] symbol '{symbols[symbol]}', it will look like this:")
    rich.print(build(exlist, symbol=symbol))
    
def demo_symbols(wait_each: float = 0.7) -> List[str]:
    """Print a demo of the symbols."""
    rich.print(
        rich.rule.Rule("[bold magenta] Symbols demo [/]")
    )
    rich.print("[bold magenta]Here's a [bold yellow]list[/]:[/]")
    some_symbols = [
        'star', 'atomstar', 'lgpoint',
        'less', 'par', 'curl',
        '6star']
    exlist = [
        {"name":"item one"},
        {"name":"item two"},
        {"name":"item three"}
    ]
    rich.print(exlist)
    rich.print(
        rich.rule.Rule()
    )
    sleep(3*wait_each)
    rich.print("[bold magenta]Here's what it looks like with different symbols:[/]")
    sleep(wait_each)
    for symbol in some_symbols:
        print_demo(symbol, exlist)
        sleep(wait_each)
        
    return some_symbols
        
def demo_themes(wait_each: float = 0.5) -> List[str]:
    """Print a demo of the themes."""
    rich.print(
        rich.rule.Rule("[bold magenta] Themes demo [/]")
    )
    rich.print("[bold magenta]Here's a [bold yellow]dictionary[/]:[/]")
    some_themes = ['default', 'pink', 'bright-blue-green', 'purple-blue']
    exobj = {
        "key A": "value A",
        "key B": ["item one", "item two"],
        "key C" : {
            "key C1": "value C1",
            "key C2": "value C2",
            "key C3": {
                "last key": "last value"
            }
        }
    }
    rich.print(exobj)
    rich.print(
        rich.rule.Rule()
    )
    sleep(3*wait_each)
    rich.print("[bold magenta]Here's what it looks like with different themes:[/]")
    sleep(wait_each)
    for theme in some_themes:
        rich.print(f"[bold magenta]Theme: [bold yellow]{theme}[/][/]")
        rich.print(build(exobj, theme=theme))
        rich.print(
            rich.rule.Rule()
        )
        sleep(wait_each)        
    return some_themes


def colorTable() -> None:
    """Print a color table."""
    table = rich.table.Table(
        show_header=True,
        header_style="bold magenta",
        title="Available Colors",
        border_style="magenta",
        box=rich.box.ROUNDED,)
    
    table.add_column("Color")
    table.add_column("Code")
    table.add_column("Example")
    table.add_column("Name")
    table.add_column("Syntaxe", justify="right", no_wrap=True)
    
    for idx in range(256):
        c = Color.from_ansi(idx)
        table.add_row(
            Panel("", style=f"on {c.name}"),
            str(idx),
            f"[color({idx})] I love colors[/]",
            f"[color({idx})] {c.name}[/]",
            r"\[color({" + str(idx) + r"})] My sentence \[/]",
        )
    return table



def themeTable() -> None:
    """Print a theme table.
    Themes are made of 4 colors for higher layers, and 1
    unique color for the lowest layer."""
    table = rich.table.Table(
        show_header=True,
        header_style="bold magenta",
        title="Available Themes",
        border_style="magenta",
        box=rich.box.ROUNDED,)
    
    demo_obj = {
        "key A": "value A",
        "key B": ["item one", "item two"],
        "key C" : {
            "key C1": "value C1",
            "key C2": "Finishing the demo"
            }
    }
    
    table.add_column("Node: First Layer")
    table.add_column("Node: Second Layer")
    table.add_column("Node: Third Layer")
    table.add_column("Node: Fourth Layer")
    table.add_column("Leaf: Layer for values")
    table.add_column("Theme representation")
    table.add_column("Theme name")
    
    for name in themes:
        leaf = themes[name]["leaf"]
        nodes = themes[name]["node"]
        table.add_row(
            Panel(f"{nodes[0]}", style=f"on {nodes[0]}"),
            Panel(f"{nodes[1]}", style=f"on {nodes[1]}"),
            Panel(f"{nodes[2]}", style=f"on {nodes[2]}"),
            Panel(f"{nodes[3]}", style=f"on {nodes[3]}"),
            Panel(f"{leaf}", style=f"on {leaf}"),
            Panel(build(demo_obj, theme=name), expand=False, width=40),
            "[bold magenta]" + name + "[/]"
        )
    
    return table