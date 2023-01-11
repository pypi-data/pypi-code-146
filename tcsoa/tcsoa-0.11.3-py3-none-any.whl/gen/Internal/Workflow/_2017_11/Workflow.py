from __future__ import annotations

from typing import Dict, List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateWorkflowInput(TcBaseObj):
    """
    input structure to create workflow process.
    
    :var processName: Name of the workflow process to be created.
    :var processDescription: Longer description of the purpose of the workflow process to be created.
    :var processTemplateName: Name of the process template. This must be a valid, existing process template.
    :var attachments: List of atachments representing either target or reference objects that will be added at process
    creation time. List may consist of target attachments or reference attachments or a mixture of both.
    :var attachmentTypes: Identifies the types of attachments listed in attachment.  Valid types include
    EPM_target_attachment (target attachment) and EPM_reference_attachment (reference attachment). There is a
    one-to-one correspondence between the attachment types on this list and the attachements list.
    :var processAssignmentList: Name of the process assignment list.
    :var additonalData: Map of property name( key ) and the property values( value )  in string format. This input is
    currently not processed and  
    added for future use.
    """
    processName: str = ''
    processDescription: str = ''
    processTemplateName: str = ''
    attachments: List[str] = ()
    attachmentTypes: List[int] = ()
    processAssignmentList: str = ''
    additonalData: KeyValuePair = None


"""
Structure for passign data in form of key and values.
"""
KeyValuePair = Dict[str, List[str]]
