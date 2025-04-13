from decimal import Decimal
from pydantic import BaseModel


class AccountData_DTO(BaseModel):
    address: str
    bandwidth: int
    energy: int
    trx: Decimal
