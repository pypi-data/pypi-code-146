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