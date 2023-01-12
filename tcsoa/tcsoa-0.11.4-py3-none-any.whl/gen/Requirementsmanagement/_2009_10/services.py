from __future__ import annotations

from typing import List
from tcsoa.gen.Requirementsmanagement._2009_10.RequirementsManagement import StdNoteInput, SetStdNoteDetails, SetStdNoteResponse, OpenStdNoteResponse
from tcsoa.base import TcService


class RequirementsManagementService(TcService):

    @classmethod
    def openStdNote(cls, input: List[StdNoteInput]) -> OpenStdNoteResponse:
        """
        This operation helps to open Fnd0ParamReqment object, or its Revision Fnd0ParamReqmentRevision contents in
        Teamcenter MS Word view. User will get the note text associated with the selected Fnd0ParamReqmentRevision
        allowing editing in that view. Opening Fnd0ParamReqment/ Fnd0ParamReqmentRevision happens in two different ways:
        1.    In context with 'Fnd0ListsParamReqments' relation: In this case, operation gives the Parameter/ value
        pairs selected in context for the parent object of 'Fnd0ListsParamReqments', allowing editing the values.
        2.    Without context: In this case, it gives note text associated for the Fnd0ParamReqmentRevision for
        view/edit purpose.
        
        
        Use cases:
        1.    Suppose user created Fnd0ParamReqment object, and now wants to see/edit note text of it, then opening
        Teamcenter MS Word view, user will see it, and can edit it.
        2.    Suppose user has attached any Fnd0ParamReqment/Fnd0ParamReqmentRevision object to any other
        Item/ItemRevision object with 'Fnd0ListsParamReqments' relation, and now wants to edit/view parameter values
        which are set while attaching this Fnd0ParamReqment/Fnd0ParamReqmentRevision, then opening Teamcenter MS Word
        view will show it.
        """
        return cls.execute_soa_method(
            method_name='openStdNote',
            library='Requirementsmanagement',
            service_date='2009_10',
            service_name='RequirementsManagement',
            params={'input': input},
            response_cls=OpenStdNoteResponse,
        )

    @classmethod
    def setStdNote(cls, input: List[SetStdNoteDetails]) -> SetStdNoteResponse:
        """
        Sets the parameters and their values on Standard Note/Parametric Requirement.  This SOA operation can set
        values on one or more Standard Note/Parametric Requirement in one operation call. When any Standard
        Note/Parametric Requirement attached to any ItemRevision it will get attached with relation
        Fnd0ListsParamRequirements (Parametric Requirements Lists). In that context if that Standard Note/Parametric
        Requirement object is selected, and edited in MS Word view, then saving of editing values from this view will
        be set on this Standard Note/Parametric Requirement using this SOA. This SOA will set those parameters and
        their values on given relation object.
        
        Use cases:
        You can edit, and set Standard Note/Parametric Requirement Parameter values using MS Word view in Teamcenter.
        This view can be launched using Window->Show view->Other->Teamcenter->MS Word
        """
        return cls.execute_soa_method(
            method_name='setStdNote',
            library='Requirementsmanagement',
            service_date='2009_10',
            service_name='RequirementsManagement',
            params={'input': input},
            response_cls=SetStdNoteResponse,
        )
