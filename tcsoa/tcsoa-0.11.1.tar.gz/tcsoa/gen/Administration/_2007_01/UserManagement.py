from __future__ import annotations

from tcsoa.gen.BusinessObjects import User, Group, Discipline, Role
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateDisciplinesIn(TcBaseObj):
    """
    This structure holds a DisciplineObject object which specifies the values of a new Discipline object. as well as
    the parent group for the new discipline.
    
    :var discipline: The object with initial data for the creation of a new Discipline object.
    :var group: The parent group of the new Discipline object.
    :var role: The role for the Discipline object. However it is not currently supported by this operation.
    """
    discipline: DisciplineObject = None
    group: Group = None
    role: Role = None


@dataclass
class CreateDisciplinesOutput(TcBaseObj):
    """
    This structure holds the newly created Discipline object and corresponding client ID.
    
    :var clientId: Identifying string from the source DisciplineObject.
    :var discipline: The new Discipline object created in this operation.
    """
    clientId: str = ''
    discipline: Discipline = None


@dataclass
class CreateDisciplinesResponse(TcBaseObj):
    """
    This structure holds a list of newly created Discipline objects.
    
    :var output: List of CreateDisciplinesOutput objects, one for each CreateDisciplinesIn object.
    :var serviceData: The object which holds the partial errors that occurred during creation of new Discipline objects
    with all newly created discipline object in its created object list.
    """
    output: List[CreateDisciplinesOutput] = ()
    serviceData: ServiceData = None


@dataclass
class DisciplineLevel(TcBaseObj):
    """
    Struct containing the discipline level name and number attribute information.
    
    :var levelName: levelName
    :var levelNumber: levelNumber
    """
    levelName: str = ''
    levelNumber: int = 0


@dataclass
class DisciplineObject(TcBaseObj):
    """
    This structure holds initial property values for a new discipline object and the corresponding client ID.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify returned CreateDisciplinesOutput
    element and partial errors associated with the DisciplineObject input.
    :var name: The name of the new Discipline object to be created.
    :var description: The description text of the new Discipline object to be created.
    :var defaultRate: The default rate property of the new Discipline object to be created.
    :var levels: The list of Discipline level.
    :var users: The list of DisciplineUser objects which specifies user members for the new Discipline to be created.
    """
    clientId: str = ''
    name: str = ''
    description: str = ''
    defaultRate: float = 0.0
    levels: List[DisciplineLevel] = ()
    users: List[DisciplineUser] = ()


@dataclass
class DisciplineUser(TcBaseObj):
    """
    This structure  holds a user and its discipline level name.
    
    :var user: The Teamcenter User object to be added to the new discipline.
    :var levelName: Not supported.
    """
    user: User = None
    levelName: str = ''
