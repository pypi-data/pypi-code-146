from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, EPMTask
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateSignoffInfo(TcBaseObj):
    """
    'CreateSignoffInfo' structure contains the requisite information to create the Signoff object. If the 'originType
    'is "SOA_EPM_SIGNOFF_ORIGIN_PROFILE" and the signoff member already exit in
    any signoff member matches the signoff profile.  
    
    :var signoffMember: Signoff member is the reviewer who needs to perform the signoff action. It can be group member,
    resource pool or an address list. 
    :var origin: Origin references the source of the signoff. When a profile signoff is added, origin references the
    signoff profile object.When a member of an address list is added as signoff, origin represents the address list to
    which the signoff member belongs.  
    :var signoffAction: Possible values are 
    "SOA_EPM_Review"
     -This values specifies that the signoff needs to be added as a review signoff.
    
    "SOA_EPM_Acknowledge"
     -This value specifies that the signoff needs to be addaed as a acknowledge signoff.
     
    "SOA_EPM_Notify" 
     -This value specifies that the signoff needs to be addaed as a notify signoff.
    
    "SOA_EPM_ACTION_UNDEFINED"
     -This value should not be used in parameter, else an error would be returned.  
    
    :var originType: For profile signoff use case , the 'originType' is "SOA_EPM_SIGNOFF_ORIGIN_PROFILE" and for subset
    of addresslist use case , the 'originType' is "SOA_EPM_SIGNOFF_ORIGIN_ADDRESSLIST". 
    
    Possible string values:
    "SOA_EPM_ORIGIN_UNDEFINED"
      -This value specifies that the origin value is NULL or not defined.
    
    "SOA_EPM_SIGNOFF_ORIGIN_PROFILE"
      -This value is specifies that the origin value is the signoff profile object.
    
    "SOA_EPM_SIGNOFF_ORIGIN_ADDRESSLIST"
      -This value is specifies that the origin value is an address list object
              
    :var signoffRequired: string which indicates whether the added reviewer decision is required or optional while
    performing signoff.
    
    
    Possible values are
    "SOA_EPM_SIGNOFF_OPTIONAL"
    -sets the property to Optional. sign off decision is not required as long as quorum is met and can be manualy
    overridden to "Required Modifiable" before perform signoff task starts.
    
    "SOA_EPM_SIGNOFF_REQUIRED_MODIFIABLE"
    - sets the property to "Required Modifiable". sign off decision is required even if quorum is met and can be
    manually overriden back to "Optional" before perform signoff task starts.
    
    "SOA_EPM_SIGNOFF_REQUIRED_UNMODIFIABLE"
    - sets the property to "Required Unmodifiable"  signoff decision is required even if quorum is met and cannot be
    manually overridden to "Optional" before perform signoff task starts.
    
    
    
    
     
    """
    signoffMember: BusinessObject = None
    origin: BusinessObject = None
    signoffAction: str = ''
    originType: str = ''
    signoffRequired: str = ''


@dataclass
class CreateSignoffs(TcBaseObj):
    """
    'CreateSignoffs' structure contains the workflow task for which Signoff needs to be added and information to create
    the Signoff objects like the Signoff Member and references like Signoff Profile or address list. 
    
    :var task: Workflow task object to which the Signoff need to be added
    :var signoffInfo: The required information to create the Signoff object
    """
    task: EPMTask = None
    signoffInfo: List[CreateSignoffInfo] = ()
