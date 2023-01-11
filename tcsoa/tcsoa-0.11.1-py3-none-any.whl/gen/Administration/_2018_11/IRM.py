from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class GetSessionInfoFromTicketResponse(TcBaseObj):
    """
    Structure that holds the user, session information and service data. The user and session information is captured
    in the call to the related getSessionInfoTicket and will be decoded from the encrypted sessionInfoTicket input
    string.
    
    :var userInfo: User login information, like: userId, userUid, groupName, groupUid, roleName, roleUid, projectId,
    projectUid
    :var sessionValues: sessionValues
    :var siteId: Site identifier that generated the ticket.
    :var serviceData: ServiceData  in which the partial errors are communicated to the client.
    """
    userInfo: UserInfo = None
    sessionValues: SessionValuesMap2 = None
    siteId: int = 0
    serviceData: ServiceData = None


@dataclass
class GetSessionInfoTicketResponse(TcBaseObj):
    """
    GetSessionInfoTicketResponse structure contains an encrypted ticket which has to be used to retrieve session info.
    
    :var sessionInfoTicket: An encrypted ticket in string format. Client can preserve this ticket and pass this ticket
    to getSessionInfoFromTicket to get the session info back.
    :var serviceData: ServiceData in which the partial errors are communicated to the client.
    """
    sessionInfoTicket: str = ''
    serviceData: ServiceData = None


"""
session values map2
"""
SessionValuesMap2 = Dict[str, List[str]]


"""
User login information, like: user_id, user_uid, group_id, group_uid, user_role_id, user_role_uid, user_project_id, user_project_uid.
"""
UserInfo = Dict[str, str]
