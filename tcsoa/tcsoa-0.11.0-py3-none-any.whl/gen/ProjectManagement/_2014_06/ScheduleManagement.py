from __future__ import annotations

from tcsoa.gen.BusinessObjects import ResourcePool, ImanRelation, User, Fnd0Qualification, Discipline
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FilterCriteria(TcBaseObj):
    """
    The filter criteria for retrieving the list of matching Users.
    
    :var disciplines: A list of Discipline object for which User needs to be filtered.
    :var grouprole: A list of ResourcePool objects from which the Group and Role information is taken for filtering the
    User.
    :var qualifications: List of  criteria specifying detailed information of the Fnd0Qualification assignments for
    which the user needs to be filtered.
    """
    disciplines: List[Discipline] = ()
    grouprole: List[ResourcePool] = ()
    qualifications: List[QualificationInfo] = ()


@dataclass
class FilteredUser(TcBaseObj):
    """
    Individual User objects which match the input filter criteria of Discipline, Group, Role and Fnd0Qualification.
    
    :var user: The User matching the filter criteria.
    :var discipline: The Discipline that the user is a part of.
    :var groupRole: The Group/Role that the user is a part of.
    :var qualificationRel: The Fnd0Qualification which is assigned to the User.
    """
    user: User = None
    discipline: Discipline = None
    groupRole: ResourcePool = None
    qualificationRel: ImanRelation = None


@dataclass
class FilteredUsersInfo(TcBaseObj):
    """
    The structure which contains list of User objects which match the input filter criteria of Discipline, Group, Role
    and Fnd0Qualification. If there are no User objects found which match the input filter criteria, an empty response
    is returned.
    
    :var filtereduserinfo: A list containing information about the filtered Users.
    :var servicedata: Service Data
    """
    filtereduserinfo: List[FilteredUser] = ()
    servicedata: ServiceData = None


@dataclass
class QualificationInfo(TcBaseObj):
    """
    List of  criteria specifying detailed information of the Fnd0Qualification assignments for which the user needs to
    be filtered
    
    
    :var qualification: The Fnd0Qualification object for which User needs to be filtered. 
    :var level: Level of Fnd0Qualification at which Users needs to be filtered.Level is defined on Fnd0Qualification
    object by the Administrator who creates the Fnd0Qualification objects.
    (for example "Advanced" , "Beginner").
    
    :var isfindAlternates: If true the operation returns all the Users who are on the same level as specified in the
    input and also the Users who are on a higher level than the level specified in the input.
    If false the operation returns only the Users who are on the exact level as specified in the input.
    """
    qualification: Fnd0Qualification = None
    level: str = ''
    isfindAlternates: bool = False
