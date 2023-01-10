from __future__ import annotations

from tcsoa.gen.Internal.ActiveWorkspaceBom._2018_05.OccurrenceManagement import DuplicateAndReplaceData, RemoveSubstitutesData, AddSubstitutesData
from tcsoa.gen.BusinessObjects import BusinessObject, Awb0Element, WorkspaceObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class OccurrenceManagementService(TcService):

    @classmethod
    def addSubstitutes(cls, inputData: AddSubstitutesData) -> ServiceData:
        """
        Adds objects as substitutes to the selected object. Substitute components are parts that are interchangeable
        with a particular component in an assembly.
        """
        return cls.execute_soa_method(
            method_name='addSubstitutes',
            library='Internal-ActiveWorkspaceBom',
            service_date='2018_05',
            service_name='OccurrenceManagement',
            params={'inputData': inputData},
            response_cls=ServiceData,
        )

    @classmethod
    def duplicateAndReplace(cls, inputData: DuplicateAndReplaceData) -> ServiceData:
        """
        This operation creates duplicate of input Awb0Element objects and structure below it. Input Awb0Element objects
        gets replaced with newly created duplicate objects.
        """
        return cls.execute_soa_method(
            method_name='duplicateAndReplace',
            library='Internal-ActiveWorkspaceBom',
            service_date='2018_05',
            service_name='OccurrenceManagement',
            params={'inputData': inputData},
            response_cls=ServiceData,
        )

    @classmethod
    def duplicateAndReplaceAsync(cls, inputData: DuplicateAndReplaceData) -> None:
        """
        This operation creates duplicate of input Awb0Element objects and structure below it. Input Awb0Element objects
        get replaced with newly created duplicate objects asynchronously. The user can perform other tasks while the
        operation will run in background. After the task is performed, the method will create a message and send it as
        a notification to the user performing the task.
        """
        return cls.execute_soa_method(
            method_name='duplicateAndReplaceAsync',
            library='Internal-ActiveWorkspaceBom',
            service_date='2018_05',
            service_name='OccurrenceManagement',
            params={'inputData': inputData},
            response_cls=None,
        )

    @classmethod
    def preferSubstitute(cls, occurrence: BusinessObject, preferredSubstitute: WorkspaceObject) -> ServiceData:
        """
        Sets the object as preferred for the input occurrence. The content is saved during the operation.
        
        Use cases:
        In an assembly there can be multiple substitutes of an occurrence. From the substitutes there can be one
        preferred substitue, the user can call preferSubstitute operation and pass in the occurrence and selected
        substitute to mark as preferred substitute.
        """
        return cls.execute_soa_method(
            method_name='preferSubstitute',
            library='Internal-ActiveWorkspaceBom',
            service_date='2018_05',
            service_name='OccurrenceManagement',
            params={'occurrence': occurrence, 'preferredSubstitute': preferredSubstitute},
            response_cls=ServiceData,
        )

    @classmethod
    def removeElements(cls, elementsToRemove: List[Awb0Element]) -> ServiceData:
        """
        This operation removes Awb0Element objects from the content or Awb0SavedBookmark. 
        The product is implicitly saved after removing Awb0Element objects. When product(s) is removed from
        Awb0SavedBookmark user needs to explicitly save the changes.User must have WRITE privilege to remove elements.
        """
        return cls.execute_soa_method(
            method_name='removeElements',
            library='Internal-ActiveWorkspaceBom',
            service_date='2018_05',
            service_name='OccurrenceManagement',
            params={'elementsToRemove': elementsToRemove},
            response_cls=ServiceData,
        )

    @classmethod
    def removeSubstitutes(cls, inputData: RemoveSubstitutesData) -> ServiceData:
        """
        Removes specified substitutes for the input element. The changes are implicitly saved after removing
        substitutes. User must have WRITE privilege to remove substitutes.
        """
        return cls.execute_soa_method(
            method_name='removeSubstitutes',
            library='Internal-ActiveWorkspaceBom',
            service_date='2018_05',
            service_name='OccurrenceManagement',
            params={'inputData': inputData},
            response_cls=ServiceData,
        )
