from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Cad._2020_01.AppSessionManagement import CreateOrUpdateSessionResponse, OpenSavedSessionFilter, OpenSessionResponse, SessionInfo
from typing import List
from tcsoa.base import TcService


class AppSessionManagementService(TcService):

    @classmethod
    def openSavedSession(cls, sessionsToOpen: List[BusinessObject], filter: OpenSavedSessionFilter) -> OpenSessionResponse:
        """
        This operation is used to open the documents and product structures that were saved to a session object using
        'createOrUpdateSavedSession'.  For product structures, the configuration rules persisted with the session are
        used to recreate the correct BOM system configuration in effect when the session was last authored.  The client
        can either open all the documents and product structures associated to the session or selectively open by
        providing 'OpenSavedSessionFilter'. The session object type that can be opened by this operation is
        Fnd0AppSession.
        
        Use cases:
        The user may have opened multiple product structures, applied search filters on them and along with  it  may
        have opened other objects like Dataset or Form. The user then issues a save session command to capture the
        state of the session so that it can be restored for continuation of work or share it other users with review
        markups. 
        
        The mechanism for a client application(CAD) which captures the CAD related session setting in a session file
        and saves the opened products, documents and its state in Teamcenter as session, contains steps as below.
        
        1.    User opens product structures, Dataset, creates a review markup and saves the session.
        2.    Client application creates a Dataset that will contain the session assets information like Markup,
        Snapshot etc. using 'createDatasets'. The client application then invokes the 'createOrUpdateSavedSession'
        where the input are the objects that were opened in the session and Dataset containing session assets. This
        step creates the session object and associates the input objects to the session with relevant relations as per
        the data model. Associated Dataset and ImanFile objects are then accessible to other authorized clients through
        the PLM system.
        3.    Another user could search for the session created in step 2 and issue a command in the application to
        open the session. The client application now invokes this operation to get all the objects and product
        structures that were associated to the session and present it to the user the way he persisted those in
        Teamcenter. The stable Id that uniquely identifies the association of a product structure or object to the
        session is also returned so that it can used to update the session when the user modifies the session.
        """
        return cls.execute_soa_method(
            method_name='openSavedSession',
            library='Cad',
            service_date='2020_01',
            service_name='AppSessionManagement',
            params={'sessionsToOpen': sessionsToOpen, 'filter': filter},
            response_cls=OpenSessionResponse,
        )

    @classmethod
    def createOrUpdateSavedSession(cls, sessionsToCreateOrUpdate: List[SessionInfo]) -> CreateOrUpdateSessionResponse:
        """
        This operation creates or updates a session data model that captures product structure configuration rules, non
        structure object references (e.g. 2D drawings), and application specific data (e.g. markups, snaphsots) from a
        visualization enabled application. The session model is a Fnd0AppSession(Session) Object referencing objects
        opened in client applications. The operation returns unique, copy stable ids for all the objects referenced by
        the session for persistence of it into CAD session files. Client specific objects can be associated to
        Fnd0AppSession with GRM relations or as sub class Fnd0ProductSessionData where the fnd0OwningObject property is
        referencing Fnd0AppSession.
        
        Use cases:
        The user may have opened multiple product structures, applied search filters on them and along with  it  may
        have opened other objects like Dataset or Form. The user then issues a save session command to capture the
        state of the session so that it can be restored for continuation of work or share it other users with review
        markups. 
        
        The mechanism for a client application(CAD) which captures the CAD related session setting in a session file
        and saves the opened products, documents and its state in Teamcenter as session, contains steps as below.
        
        User creates a Session
        - User opens product structures, Dataset, creates a review markup and saves the session.
        - Client application creates a Dataset that will contain the session assets information like Markup, Snapshot
        etc. using 'createDatasets' or using 'BaseObjectAttachInfo.baseObjectToCreateOrUpdate'. 
        - The client application then invokes the 'createOrUpdateSavedSession' where the input are the objects that
        were opened in the session and Dataset containing session assets. This step creates the session object and
        associates the input objects to the session with relevant relations as per the data model. Associated Dataset
        and ImanFile objects are then accessible to other authorized clients through the PLM system.
        
        
        
        User updates a Session
        - User searches for the Fnd0AppSession he has saved.
        - Opens it in the client application that supports opening of Fnd0AppSession.
        - The client application invokes 'openSavedSession' operation which returns the objects associted to the
        session with its corresponding stable Ids.
        - The application restores his session as persisted by the Fnd0AppSession.
        - User now closes some documents, opens new documents and/or modifes existing objects.
        - User now issues a command to save the session
        - The application invokes 'createOrUpdateSavedSession' operation to update the object association to the
        session by identifying the association via stable Id. 
        
        
        
        Note: As a best practice, if the configuration or search recipe of a product structure in an existing session
        is changed and saved by the user it is recommended that the application removes the the product structure from
        the session and adds the changed product structure to the session with the same stableId or using a new stable
        id.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateSavedSession',
            library='Cad',
            service_date='2020_01',
            service_name='AppSessionManagement',
            params={'sessionsToCreateOrUpdate': sessionsToCreateOrUpdate},
            response_cls=CreateOrUpdateSessionResponse,
        )
