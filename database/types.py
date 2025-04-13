from datetime import datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field


class AccountData(SQLModel, table=True):
    id: int = Field(primary_key=True)
    request_datetime: datetime = Field(nullable=False)
    address: str
    bandwidth: int
    energy: int
    trx: Decimal
