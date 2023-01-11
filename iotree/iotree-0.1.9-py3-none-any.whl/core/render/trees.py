import rich
from time import sleep

from rich.tree import Tree
from itertools import cycle
from typing import (
    Any, Dict, List, Union,
    Optional, Tuple, MutableMapping,
    MutableSequence
    )


from iotree.core.render.theme import (
    initConfig, convertTheme, check_none, lnode
)

from iotree.core.render.funcs import (
    format_user_theme, apply_progress_theme,
)

from iotree.utils.paths import (
    package_dir, base_dir, config_dir, safe_config_load
)

symbols, themes, user_infos, local_config = safe_config_load()


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
        
    if isinstance(dictlike, (list, MutableSequence)):
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
    elif isinstance(dictlike, (dict, MutableMapping)):
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
        if not isinstance(dictlike, (str, float, int)):
            raise TypeError(f"Expected a dictionary or list of dictionaries, got {type(dictlike)}")
        state.add(f"[{leaf_color}] {dictlike}[/]")
    return state