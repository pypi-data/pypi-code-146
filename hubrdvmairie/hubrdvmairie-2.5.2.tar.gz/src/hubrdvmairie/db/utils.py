from typing import List

from ..core.config import get_settings
from ..models.editor import Editor
from ..models.municipality import Municipality


def get_all_editors() -> List[Editor]:
    """
    Get global editors from the settings object
    """
    editors_stored: List[Editor] = get_settings().editors_list.copy()
    return editors_stored


def set_all_editors(editors: List[Editor]):
    """
    Set global editors list in the settings object
    """
    get_settings().editors_list = editors


def get_all_meeting_points() -> List[Municipality]:
    """
    Get global meeting point from the settings object
    """
    meeting_point_stored: List[Municipality] = get_settings().meeting_point_list.copy()
    return meeting_point_stored


def set_all_meeting_points(meeting_points: List[Municipality]):
    """
    Set global editors list in the settings object
    """
    get_settings().meeting_point_list = meeting_points


def get_ws_use_rates(ip_address) -> int:
    """
    Get global WebSocket use rates from the settings object for a specific ip address
    """
    if ip_address in get_settings().ws_use_rates:
        return get_settings().ws_use_rates[ip_address]
    else:
        return 0


def add_ws_use_rates(ip_address):
    """
    Add 1 to global websocket use rates list in the settings object for a specific ip address
    """
    if ip_address not in get_settings().ws_use_rates:
        get_settings().ws_use_rates[ip_address] = 0
    get_settings().ws_use_rates[ip_address] += 1


def reset_all_ws_use_rates():
    """
    Reset global websocket use rates list in the settings object
    """
    get_settings().ws_use_rates = {}
