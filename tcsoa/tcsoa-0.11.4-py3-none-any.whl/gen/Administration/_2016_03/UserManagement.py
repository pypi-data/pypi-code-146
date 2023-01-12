from __future__ import annotations

from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class DeleteUsersInput(TcBaseObj):
    """
    Input structure to delete User object.
    
    :var userId: The User ID of the User to be deleted.
    :var newOwningUser: The User ID to assign ownership of the objects currently owned by 'userId'. This value is
    ignored if 'deleteObjects' is true. A value must be provided if 'deleteObjects' is false.
    :var newOwningGroup: The name of the Group to assign Group ownership of object currently owned by the 'userId'. The
    'newOwningUser' must be a member of this group.The Group name is ignored if 'deleteObjects' is true. If
    'deleteObjects' is false and value is not given then the default group of 'newOwningUser' is used.
    :var deleteObjects: If true, the objects owned by 'userId' are deleted. If false, the objects are kept and their
    ownership is transferred to 'newOwningUser' and 'newOwningGroup'.
    """
    userId: str = ''
    newOwningUser: str = ''
    newOwningGroup: str = ''
    deleteObjects: bool = False
