from dataclasses import dataclass

from checker._types import AccountData_DTO


@dataclass
class GetFromDatabaseOutput:
    pages: int
    page: int
    data: list[AccountData_DTO]
