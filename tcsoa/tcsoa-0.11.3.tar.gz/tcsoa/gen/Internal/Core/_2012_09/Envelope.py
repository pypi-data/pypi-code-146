from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, User
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class EmailInfo(TcBaseObj):
    """
    This structure stores email related information.
    
    :var subject: The subject of email message.
    :var messageBody: The body of the email message.
    :var listOfRecipients: List of internal Teamcenter recipients. These recipients can be users, groups and address
    lists. Email will be sent to all the users representing the recipients based on the email address provided. If
    there is no email address specified for any user, email will be sent to the OS user name for the user.
    :var listOfCcRecipients: List of internal Teamcenter CC recipients. These recipients can be users, groups and
    address lists. Email will be sent to all the users representing the recipients based on the email address provided.
    If there is no email address specified for any user, email will be sent to the OS user name for the user.
    :var listOfExtRecipients: List of external recipients' email addresses.
    :var listOfExtCcRecipients: CC recipients' email addresses.
    :var fmsReadTickets: FMS read tickets for the files to be attached to the email. This is an optional parameter.
    :var sender: The sender of the email message. The sender is a Teamcenter user.
    :var clientID: ID to uniquely identify the email transaction.
    """
    subject: str = ''
    messageBody: str = ''
    listOfRecipients: List[BusinessObject] = ()
    listOfCcRecipients: List[BusinessObject] = ()
    listOfExtRecipients: List[str] = ()
    listOfExtCcRecipients: List[str] = ()
    fmsReadTickets: List[str] = ()
    sender: User = None
    clientID: str = ''
