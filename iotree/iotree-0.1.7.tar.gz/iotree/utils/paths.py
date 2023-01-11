import json
from pathlib import Path
from typing import Dict, Any, Tuple, Union, List, Callable

utils_dir = Path(__file__).parent
package_dir = utils_dir.parent
base_dir = package_dir.parent
tests_dir = base_dir / 'tests'
config_dir = package_dir / 'config'

def safe_json_load(path: Union[str, Path]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Load a file or directory of files."""
    path = Path(path)
    if path.exists():
        if path.is_dir():
            return [json.load(open(file, 'r')) for file in path.iterdir()].pop()
        else:
            return json.load(open(path, 'r'))
    else:
        return {}

def safe_config_load() -> Tuple[Dict[str, Any]]:
    """Load config files.
    
    In this specific order:
    - symbols.json
    - themes.json
    - user-settings.json
    - local-config.json
    """
    sym_path = config_dir / 'symbols.json'
    themes_path = config_dir / 'themes.json'
    uinfo_path = config_dir / 'user-settings.json'
    lconf_path = config_dir / 'local-config.json'
    
    symbols = safe_json_load(sym_path)
    themes = safe_json_load(themes_path)
    user_infos = safe_json_load(uinfo_path)
    local_config = safe_json_load(lconf_path)
    
    return symbols, themes, user_infos, local_config
