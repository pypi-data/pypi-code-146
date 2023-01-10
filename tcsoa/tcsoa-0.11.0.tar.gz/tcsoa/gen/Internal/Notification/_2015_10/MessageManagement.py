from __future__ import annotations

from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class UnreadMessages(TcBaseObj):
    """
    A list of Fnd0Message UID for the unread messages.
    
    :var messages: The list of Fnd0Message UIDs.
    """
    messages: List[str] = ()
