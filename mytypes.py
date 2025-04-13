from datetime import datetime
from pydantic import BaseModel

from checker._types import AccountData_DTO


class GetAddressOutput(BaseModel):
    time: datetime
    account_data: AccountData_DTO


class GetAddressInput(BaseModel):
    address: str


class GetLastDataOutput(BaseModel):
    page: int
    data: list[AccountData_DTO]
