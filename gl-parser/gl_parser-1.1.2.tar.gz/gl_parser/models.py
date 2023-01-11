from decimal import Decimal
from typing import Dict, Any, Optional

from pydantic import BaseModel, Field
from datetime import date
from gl_parser import CONFIGURATION_MANAGER

DEFAULT_COLUMN_MAPPINGS = CONFIGURATION_MANAGER.get_current()['parsers']['column_mappings']

DEFAULT_START_ROW = CONFIGURATION_MANAGER.get_current()['parsers']['start_row']

DEFAULT_SHEET_NAME = CONFIGURATION_MANAGER.get_current()['parsers']['sheet_name']


class ParserConfig(BaseModel):
    sheet_name: str = Field(default=DEFAULT_SHEET_NAME)
    start_row: int = Field(default=DEFAULT_START_ROW)
    column_mappings: Dict[str, Dict[str, Any]] = Field(default=DEFAULT_COLUMN_MAPPINGS)


class Transaction(BaseModel):
    account_id: Optional[str] = Field(description="Unique account id")
    account_description: Optional[str] = Field(description="Account description")
    date: Optional[date]  # = Field(description='Date of the transaction')
    reference: Optional[str] = Field(description="Reference")
    journal: Optional[str] = Field(description="Journal")
    description: str = Field(description="Transaction description")
    debit_amount: Optional[Decimal] = Field(description="Debit amount")
    credit_amount: Optional[Decimal] = Field(description="Credit amount")
    balance: Optional[Decimal] = Field(description="Credit amount")
