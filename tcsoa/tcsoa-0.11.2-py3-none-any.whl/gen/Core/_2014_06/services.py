from __future__ import annotations

from tcsoa.gen.Core._2014_06.DigitalSignature import ApplySignaturesInputData, VoidSignaturesInputData, GetSignatureMessagesResponse
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from tcsoa.gen.Core._2011_06.DataManagement import TraceabilityInfoInput
from tcsoa.gen.Core._2012_10.DataManagement import TraceabilityInfoInput1
from tcsoa.gen.Core._2014_06.DataManagement import TraceabilityReportOutput2, TraceabilityReportOutputLegacy


class DigitalSignatureService(TcService):

    @classmethod
    def getSignatureMessages(cls, targetObject: List[BusinessObject]) -> GetSignatureMessagesResponse:
        """
        This operation returns signature messages for a list of business objects. These signature messages are used by
        SOA framework method  com.teamcenter.soa.client.PKCS7.sign     API to generate CMS string (Cryptographic
        Message Syntax). The operation response GetSignatureMessagesResponse contains details of signature messages
        computed for each of the input business objects along with the ServiceData. The attributes that are to be used
        for signature message computation are configured using the business object constant
        Fnd0DigitalSignatureAttributes and Fnd0DigitalSignatureChildObjects.
        """
        return cls.execute_soa_method(
            method_name='getSignatureMessages',
            library='Core',
            service_date='2014_06',
            service_name='DigitalSignature',
            params={'targetObject': targetObject},
            response_cls=GetSignatureMessagesResponse,
        )

    @classmethod
    def voidSignatures(cls, input: List[VoidSignaturesInputData], electronicSignature: str) -> ServiceData:
        """
        This operation voids the selected digital signatureson a given target object.. The details of  the electronic
        signature may be obtained by calling the requisite SOA framework method com.teamcenter.soa.client.PKCS7.sign.
        ..This is provided as input to the voidDigitalSignatures opearation along with the other inputs. Successful
        completion of the operation, is an indication that the selected digital signature objects have been voided for
        the input business object.
        
        Use cases:
        After applying a digital signature,the object is locked for modification and users would not be able to modify
        any of the attribute values. In certain conditions, the current values on the object would need to be updated
        and the digital signature would need to be reapplied with the updated set of values. To achieve this, the
        existing digital signatures on the object are voided and  required values are updated . After all the updates
        are complete,  digital signature is reapplied on the object. It is to be noted that if all the Digital
        Signatures on an object are voided, then the object state is equivalent to not having any digital signature
        applied and is open for updates 
        """
        return cls.execute_soa_method(
            method_name='voidSignatures',
            library='Core',
            service_date='2014_06',
            service_name='DigitalSignature',
            params={'input': input, 'electronicSignature': electronicSignature},
            response_cls=ServiceData,
        )

    @classmethod
    def applySignatures(cls, input: List[ApplySignaturesInputData]) -> ServiceData:
        """
        This operation applies digital signature to a list of Business objects provided in the input. The operation
        input is a list of DigitalSignatureInput structures. Each structure in this list consists of details pertaining
        to the Business Object and its corresponding CMS (Cryptographic Message Syntax). Digital Signature is allowed
        to be applied on business objects for which the business object constant Fnd0AllowDigitalSignature is enabled.
        
        Use cases:
        To apply digital signature from RAC, the operation getSignatureMessages should first be called to compute the
        signature messages for the input business objects. This should be followed by a call to the SOA framework
        method com.teamcenter.soa.client.PKCS7.sign , which takes signature message as input and provides the encrypted
        string as output. The encrypted string is passed as input to the operation applyDigitalSignatures. Successful
        completion of the operation, is an indication that the digital signature has been applied to the input business
        object.
        """
        return cls.execute_soa_method(
            method_name='applySignatures',
            library='Core',
            service_date='2014_06',
            service_name='DigitalSignature',
            params={'input': input},
            response_cls=ServiceData,
        )


class DataManagementService(TcService):

    @classmethod
    def getTraceReport2(cls, input: List[TraceabilityInfoInput1]) -> TraceabilityReportOutput2:
        """
        This operation generates a Trace Report for the input objects.  The report will contain information about
        complying as well as defining objects which are connected to input object using FND_TraceLink, or its subtype.
        This operation checks if there is any FND_TraceLink relation starting or ending from input object(s). If
        FND_TraceLink relation exists for input object(s), then it gets the other end of FND_TraceLink relation and
        generates a trace report. 
        
        Trace links can be between following objects:
        1  Between occurrences of an ItemRevision 
        2  Between any two WorkspaceObject.
        
        If scope of search structure is defined for the getting trace report in input of this operation by sending top
        lines of BOMWindow instances, then matching trace link instances within the scope windows will be returned.
        
        If input of this operation is having list of object type names, then object type filter will be applied to
        target objects of trace link.
        
        If input of this operation is having list of trace link type names, then those types of trace link will be
        returned in trace report.
        
        If property filter is given in the input of this operation, then the additional filter of property will be
        applied on the output before sending to client.
        
        Trace report tree will be sorted for given property, sort direction can also be defined, if not defined then it
        will get default sorted in ascending direction.
        
        The output of this operation can be either sent to rich client to build the report or to MSExcel application.
        
        User can export this trace report to MSExcel application by sending appropriate exportTo mode in input. If the
        mode of export is "TraceReportMSExcelExport", then trace report will be exported to .xlsm file and this file
        ticket will be sent to rich client. Then rich client will download the file and open MSExcel application.
        
        
        Use cases:
        Suppose user created trace link between Requirement R1 as start point and R2 as end point and creates trace
        link from Requirement R3 as start and R1 as end point.
        When user runs traceability report on R1 requirement he will get R2 object as complying object and R3 will come
        as defining object.
        
        If filter will be added to show only Paragraph type objects, then nothing will be returned in Trace Report as
        the type is not matching with filter.
        
        If filter will be applied to a subtype of FND_TraceLink and above trace link is of type FND_TraceLink, then
        also empty trace report will be returned, as trace link type does not match with filter trace link type vector
        from operation input.
        
        If user invokes command to export the trace report to Excel, then trace report for Requirement R1 will be
        generated and exported in .xlsm file and opened in MSExcel application.
        
        Trace link on occurences:
        Suppose user created trace link between Requirement R1 as start point and Trace Link on occurrence on part P1
        as end point by setting the P1's parent line as context line then this SOA will also return the
        PSBomViewRevision which was set as context line while creating the Trace Link.
        """
        return cls.execute_soa_method(
            method_name='getTraceReport2',
            library='Core',
            service_date='2014_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=TraceabilityReportOutput2,
        )

    @classmethod
    def getTraceReportLegacy(cls, input: TraceabilityInfoInput) -> TraceabilityReportOutputLegacy:
        """
        This operation generates a Trace Report for the input objects.  This operation returns information about
        complying as well as defining objects which are connected to selected object using FND_TraceLink or its subtype
        of GRM relation.
        
        Trace links can be between following objects:
        1.    Between occurrences of an ItemRevision
        2.    Between any two WorkspaceObject.
        
        If indirect trace report flag is set to true during this operation, then user will get trace report for
        ItemRevision if selected object is occurrence, and trace report for Items if selected objects is ItemRevision
        in addition to direct trace report for the selected object.
        
        If trace link is on occurrence then This SOA version will return PSBOMViewRevision context line information
        also.
        
        
        Use cases:
        Suppose user created trace link between Requirement R1 as start point and R2 as end point and creates trace
        link from Requirement R3 as start and R1 as end point.
        When user runs traceability report on R1 requirement he will get R2 object as complying object and R3 will come
        as defining object.
        
        TraceLink on occurrences:
        Suppose user created trace link between Requirement R1 as start point and trace link on occurrence on part P1
        as end point by setting the P1's parent line as context line then this SOA will also return the
        PSBomViewRevision which was set as context line while creating the trace link.
        
        """
        return cls.execute_soa_method(
            method_name='getTraceReportLegacy',
            library='Core',
            service_date='2014_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=TraceabilityReportOutputLegacy,
        )


class ReservationService(TcService):

    @classmethod
    def bulkCancelCheckout(cls, objects: List[BusinessObject]) -> ServiceData:
        """
        This operation cancels a check-out for a set of previously checked-out business objects in bulk. The objects
        will be restored to the pre-check-out state. Only one user can perform a cancel check-out transaction on the
        object if the user has enough privilege on the object. This action may be applied to remote checked-out
        objects, and will cancel the check-out and records the cancel check-out transaction event. Cancel checkout is
        not supported for some of the business objects for e.g. - Item, BOMView,BOMViewRevision, Schedule.
        """
        return cls.execute_soa_method(
            method_name='bulkCancelCheckout',
            library='Core',
            service_date='2014_06',
            service_name='Reservation',
            params={'objects': objects},
            response_cls=ServiceData,
        )

    @classmethod
    def bulkCheckin(cls, objects: List[BusinessObject]) -> ServiceData:
        """
        This operation checks-in a set of previously checked-out business objects in bulk. This operation takes care of
        all complex business logic involved to check-in passed in business objects. Each input object is verified that
        it is locally owned, site owned, and not transferred to another user after the checkout was performed. This
        operation validates precondition defined per type in COTS object and site customization and performs basic
        check-in. Dataset, ItemRevision and many other business object types have their own business logic for
        check-in. This operation calls underlying checkin method of those individual objects.
        
        Note: If the business object ItemRevision is checked out using reservation type
        "RES_RESERVE_BULK_WITH_DELAY_DEEP_COPY" and if the given object is not modified after it was checked out using
        this reservation type then the checkin opetation performed on this object will not increase the sequence number
        of the ItemRevision business object
        """
        return cls.execute_soa_method(
            method_name='bulkCheckin',
            library='Core',
            service_date='2014_06',
            service_name='Reservation',
            params={'objects': objects},
            response_cls=ServiceData,
        )

    @classmethod
    def bulkCheckout(cls, objects: List[BusinessObject], comment: str, changeId: str, reservationType: int) -> ServiceData:
        """
        This operation checks out a set of business objects with given comment and, change identifier in bulk fashion.
        Only one user can perform a check-out transaction on the object. The user must have sufficient privilege on the
        object or the checkout will fail. This operation allows for remote check-out and records the check-out
        transaction event. In the case where the reservationType is RES_RESERVE_BULK_WITH_DELAY_DEEP_COPY, this
        operation checks out business objects without creating the backup copy of the reserved objects. The backup copy
        will be created on demand when the reserved object is modified. This operation is faster than the checkout
        operation.
        
        Use cases:
        The object can be reserved to gain exclusive rights so that no other user can modify it while the reserver is
        modifying the given object.
        """
        return cls.execute_soa_method(
            method_name='bulkCheckout',
            library='Core',
            service_date='2014_06',
            service_name='Reservation',
            params={'objects': objects, 'comment': comment, 'changeId': changeId, 'reservationType': reservationType},
            response_cls=ServiceData,
        )
