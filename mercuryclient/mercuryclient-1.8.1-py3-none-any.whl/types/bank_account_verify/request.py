from pydantic import BaseModel
from pydantic import Field


class AccountVerifyRequest(BaseModel):

    name: str = Field(max_length=50)
    phone: str = Field(max_length=10, min_length=10)
    bank_account_number: str = Field(max_length=50)
    bank_ifsc_code: str = Field(max_length=50)
