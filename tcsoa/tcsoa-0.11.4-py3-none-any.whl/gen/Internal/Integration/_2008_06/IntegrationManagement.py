from __future__ import annotations

from tcsoa.gen.BusinessObjects import ImanFile
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class RenameIMFInfo(TcBaseObj):
    """
    Input structure that contains a clientID, file object reference, and string for rename.
    
    :var clientId: Input string to uniquely identify the input, used primarily for error handling and output mapping.
    :var file: File object to rename.
    :var name: Input string used to rename the input file.
    """
    clientId: str = ''
    file: ImanFile = None
    name: str = ''
