from __future__ import annotations

from tcsoa.gen.BusinessObjects import Fnd0Qualification, User
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AssignUserQualificationInfo(TcBaseObj):
    """
    List of  AssignUserQualificationInfo structures, each containing information required for assigning a
    Fnd0Qualification object to a Teamcenter User.
    
    
    :var user: Teamcenter User object to assign the qualification.
    :var qualification: Fnd0Qualification object to assign user qualification.
    :var levelName: Name of the Qualification level.
    :var effectiveDate: EffectiveDate for the Qualification to assign.
    :var expiryDate: Expiry Date for for the Qualification to assign.
    """
    user: User = None
    qualification: Fnd0Qualification = None
    levelName: str = ''
    effectiveDate: datetime = None
    expiryDate: datetime = None


@dataclass
class ManageQualificationInfo(TcBaseObj):
    """
    Information required to create Fnd0Qualification objects. 
    
    :var qualificationName: A unique name for the Fnd0Qualification.
    :var description: Description of the Fnd0Qualification.
    :var isExpiryDateRequired: Indicates whether effective and expiry dates are required for the Qualification. This is
    used to decide whether effective and expiry dates are required while assigning the Fnd0Quailification to a
    Teamcenter User.
    :var qualificationLevels: The levels are defined on Fnd0Qualification object as ordered list of strings. Levels
    signifies the ranking amongst the user once the Fnd0Qualification is assigned to User with a level.  Levels are
    defined by administrator. Valid values for level can be any string. For example "Advanced" , "Beginner" etc.
    """
    qualificationName: str = ''
    description: str = ''
    isExpiryDateRequired: bool = False
    qualificationLevels: List[str] = ()


@dataclass
class QualificationLevelInfo(TcBaseObj):
    """
    List of QualificationLevelInfo structures containing the Fnd0Qualification object and the level to remove.
    
    :var qualification: Fnd0Qualification object to remove qualification level.
    
    
    :var levelName: Name of Level to remove.
    """
    qualification: Fnd0Qualification = None
    levelName: str = ''


@dataclass
class RemoveUserQualificationInfo(TcBaseObj):
    """
    List of RemoveUserQualificationInfo structures, each containing the User and the Fnd0Qualification to be removed.
    
    :var user: User Object to remove qualification from the user
    :var qualification: Fnd0Qualification object to remove user qualification from the user.
    """
    user: User = None
    qualification: Fnd0Qualification = None


@dataclass
class UpdateQualificationInfo(TcBaseObj):
    """
    Information required to update Fnd0Qualification objects.
    
    :var qualification: Fnd0Qualification object to be updated.
    :var qualificationInfo: Qualification information to be updated.
    """
    qualification: Fnd0Qualification = None
    qualificationInfo: ManageQualificationInfo = None
