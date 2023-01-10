import rich
import json
from time import sleep

from rich.tree import Tree
from itertools import cycle
from typing import Any, Dict, List, Union, Optional, Tuple

from iotree.utils.paths import (
    package_dir, base_dir, config_dir, safe_config_load
)

symbols, themes, user_infos, local_config = safe_config_load()

def convertTheme(theme_object: Union[str,Dict[str, Any]]) -> Dict[str, Any]:
    """Convert a theme name to a theme object."""
    return themes[theme_object] if isinstance(theme_object, str) else theme_object

def check_none(value):
    """Check if a value is `None` or not."""
    try:
        if value is None:
            return True
        else:
            return False
    except TypeError:
        return False

def initConfig(user: Optional[str] = None) -> List[str]:
    """Initialize the user's theme and symbol settings.
    
    Args:
        user: The user's name.
    
    Returns:
        A list of the user's theme, numbered, and symbol settings.
    """

    if user is None:
        if 'last_user' in local_config.keys():
            user = local_config['last_user']
        else:
            user = 'default'
    
    user_theme = user_infos[user]['theme']
    theme = themes[user_theme]
    symbol = user_infos[user]['symbol']
    
    return [theme, symbol]

def lnode(
    symbol: Optional[str] = '─',
    index: Optional[int] = None,
    symbols: Optional[Dict[str, str]] = symbols,
    ) -> str:
    """Return a list node symbol with an index."""
    
    paired = {
        '[':['[', ']'],
        ']':['[', ']'],
        '(':['(', ')'],
        ')':['(', ')'],
        '{':['{', '}'],
        '}':['{', '}'],
        '<':['<', '>'],
        '>':['<', '>'],
        ":":[':', ':']
    }
    if index is not None:
        if symbols[symbol] in paired.keys():
            return f"{paired[symbols[symbol]][0]}{index}{paired[symbols[symbol]][1]}"
        else:
            return f"{symbols[symbol]}:{index}"
    else:
        return symbols[symbol]

def build(
    dictlike: Union[Dict[str, Any], List[Dict[str, Any]]],
    state: Optional[Tree] = None,
    theme: Optional[Union[str,Dict[str,str]]] = None,
    symbol: Optional[str] = None,
    user: Optional[str] = None,
    numbered: Optional[bool] = False,
    depth: Optional[int] = 10,
    cyclcols: Optional[cycle] = None,
    ) -> Tree:
    """Build a tree from a dictionary or list of dictionaries.
    
    The dictionary is the result of reading a file or directory of files.
    Supported file formats: .json, .yaml, .toml
    
    Args:
        dictlike (Union[Dict[str, Any], List[Dict[str, Any]]]): A dictionary or list of dictionaries.
        state (Optional[Tree], optional): A rich.tree.Tree object. Defaults to None. Is used for recursion.
        theme (Optional[Dict[str,str]], optional): A theme from the themes.json file. Defaults to 'default'.
        symbol (Optional[str], optional): A symbol from the symbols.json file. Defaults to 'star'.
        user (Optional[str], optional): A user from the user-settings.json file. Defaults to None.
        numbered (Optional[bool], optional): Whether or not to number the list nodes. Defaults to False.
        depth (Optional[int], optional): The depth of the tree. Defaults to 10. [bold red]Not yet implemented[/].
        cyclcols (Optional[cycle], optional): A cycle of colors. Defaults to None. Is used for recursion. 
    """
    theme = convertTheme(theme)
    
    if state is None:
        __theme, __symbol = initConfig(user)
        theme = __theme if check_none(theme) else theme
        symbol = __symbol if symbol is None else symbol
        node_colors = theme['node']
        leaf_color = theme['leaf']
        cyclcols = cycle(node_colors)
        _col = next(cyclcols)
        state = Tree(f'[bold {_col}]Contents[/]')
    else:
        __theme, __symbol = initConfig(user)
        theme = __theme if check_none(theme) else theme
        symbol = __symbol if symbol is None else symbol
        node_colors = __theme['node']
        leaf_color = __theme['leaf']
        
    if symbol in ['par', 'curl', 'sqbra', 'dbcol', 'less']:
        numbered = True
    else:
        numbered = False
        
    if isinstance(dictlike, list):
        _col = next(cyclcols)
        
        if numbered:
            i = 0
        for d in dictlike:
            if not isinstance(d, (dict, list)):
                state.add(f"[{leaf_color}]{d}[/]")
            else:
                if numbered:
                    _symbol = lnode(symbol, index=i)
                    i += 1
                else:
                    _symbol = lnode(symbol)
                branch = state.add(f"[bold {_col}]{_symbol}[/]")
                build(d, state=branch,
                      cyclcols=cyclcols,
                      depth=depth-1,
                      theme=theme,
                      numbered=numbered,
                      symbol=symbol,
                      user=user)
    elif isinstance(dictlike, dict):
        _col = next(cyclcols)
        for key, value in dictlike.items():
            if not isinstance(value, (dict, list)):
                state.add(f"[bold {_col}]{key}[/]:[{leaf_color}] {value}[/]")
            else:
                branch = state.add(f"[bold {_col}]{key}:[/]")
                build(value, state=branch,
                      cyclcols=cyclcols,
                      depth=depth-1,
                      theme=theme,
                      numbered=numbered,
                      symbol=symbol,
                      user=user
                      )
    else:
        state.add(f"[{leaf_color}] {value}[/]")
        
    return state


def treeThemeToTable(theme: Union[str, Dict[str, Any]] = "default"):
    """Convert a theme fit for a tree to one for a rich.table.Table object."""
    if isinstance(theme, str):
        theme = themes[theme]
    table_theme = {
        "header": theme["node"][0],
        "rows": theme["node"][1:3],
    }
    return table_theme

def recordFormatting(record: Dict[str, Any], columns: List[str]) -> Dict[str, Any]:
    """Add empty column values to a partial record + convert values to strings.
    
    Also orders the columns in the same order as the columns list."""
    lrow = []
    for col in columns:
        if col not in record.keys():
            lrow.append("")
        else:
            lrow.append(str(record[col]))
    return lrow

def tableFromRecords(
    records: List[Dict[str, Any]],
    title: Optional[str] = "Table of records",
    theme: Optional[str] = None,
    ) -> rich.table.Table:
    theme = treeThemeToTable(theme)
    tab = rich.table.Table(
        title=title,
        header_style=theme["header"],
        box=rich.box.ROUNDED,
        row_styles=theme["rows"]
        )
    columns = list(records[0].keys())
    for col in columns:
        tab.add_column(col, justify="center")
    for record in records:
        tab.add_row(*recordFormatting(record, columns))
    return tab
    


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