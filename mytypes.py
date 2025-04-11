from pydantic import BaseModel


class GetAddressOutput(BaseModel):
    address: str
    bandwidth: float
    energy: float
    trx: int


class GetAddressInput(BaseModel):
    address: str


class Data_DTO(BaseModel):
    address: str
    bandwidth: float
    energy: float
    trx: int


class GetLastDataOutput(BaseModel):
    page: int
    data: list[Data_DTO]

    # class Config:
    #     frozen = True
