import datetime
import uvicorn
from database.main import add_to_database, get_from_database
from database.types import AccountData  # noqa: F401
from mytypes import GetAddressInput, GetAddressOutput, GetLastDataOutput

from fastapi import FastAPI

from checker import get_address_data, AccountData_DTO

ELEMENTS_PER_PAGE = 10


async def check_address(input: GetAddressInput) -> GetAddressOutput:
    query_time: datetime = datetime.datetime.now()
    account_data: AccountData_DTO = get_address_data(input.address)
    add_to_database(query_time, account_data)
    result = GetAddressOutput(time=query_time, account_data=account_data)
    return result


async def get_last_data(page: int) -> GetLastDataOutput:
    # render some html
    data: list[AccountData_DTO] = [
        AccountData_DTO(
            address=model.address,
            bandwidth=model.bandwidth,
            energy=model.energy,
            trx=model.trx,
        )
        for model in get_from_database(page)
    ]
    result = GetLastDataOutput(page=page, data=data)
    return result


def main():
    app = FastAPI()

    app.post("/check_address")(check_address)  # info for address

    app.get("/get_last")(get_last_data)

    uvicorn.run(app)


if __name__ == "__main__":
    main()
