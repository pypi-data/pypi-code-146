from typing import Optional
from mercuryclient.types.bbps.enums import ComplaintType, ShopType
from mercuryclient.types.common import Pincode
from pydantic import BaseModel
from pydantic import Field


class AgentRequest(BaseModel):
    name: str = Field(max_length=50)
    contactperson: str = Field(max_length=50)
    mobileNumber: str = Field(max_length=10, min_length=10)
    agentshopname: str = Field(max_length=50)
    businesstype: ShopType
    address1: str = Field(max_length=50)
    address2: str = Field(max_length=50)
    state: str = Field()
    city: str = Field()
    pincode: Pincode
    latitude: str = Field(max_length=50)
    longitude: str = Field(max_length=50)
    email: str = Field(max_length=50)


class GetAmountRequest(BaseModel):

    billerId: str = Field(max_length=50)
    mobileNumber: str = Field(max_length=10, min_length=10)
    crno: str = Field(max_length=50)
    agentId: str = Field(max_length=50)


class BillPaymentRequestTransid(BaseModel):

    billAmount: str = Field(max_length=50)
    transid: str = Field(max_length=50)
    mobileNumber: str = Field(max_length=10, min_length=10)
    agentId: str = Field(max_length=50)
    BillerCategory: str = Field(max_length=50)
    billerId: str = Field(max_length=50)
    crno: str = Field(max_length=50)


class BillPaymentRequest(BaseModel):

    billAmount: str = Field(max_length=50)
    mobileNumber: str = Field(max_length=10, min_length=10)
    agentId: str = Field(max_length=50)
    BillerCategory: str = Field(max_length=50)
    billerId: str = Field(max_length=50)
    crno: str = Field(max_length=50)


class TxnComplaintRequest(BaseModel):
    transactionRefId: str = Field(max_length=50)
    mobileNumber: str = Field(max_length=10, min_length=10)
    reason: str = Field(max_length=70)
    description: Optional[str] = Field(max_length=70)


class ServiceComplaintRequest(BaseModel):
    billerId: str = Field(max_length=50)
    mobileNumber: str = Field(max_length=10, min_length=10)
    description: str = Field(max_length=70)
    reason: str = Field(max_length=50)
    type: str = Field(max_length=50)


class ComplaintStatusRequest(BaseModel):
    complaintType: ComplaintType
    complaintId: str = Field(max_length=50)
