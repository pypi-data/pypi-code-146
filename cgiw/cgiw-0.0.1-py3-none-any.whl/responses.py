from json import dumps
from typing import Optional, Union, Tuple, Dict

def json(obj: Optional[Union[dict, list, int, float, str, bool]]) -> Tuple[str, Dict[str, str], str]:
    return ('200 OK', {'Content-Type': 'application/json'}, dumps(obj))

def redirect(url: str) -> Tuple[str, Dict[str, str], str]:
    headers = {
        'Content-Type': 'text/plain',
        'Location': url
    }
    return ('301 Moved Permanently', headers, 'Redirecting...')