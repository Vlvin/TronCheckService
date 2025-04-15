from dataclasses import dataclass
import datetime
import uvicorn

from database import add_to_database, get_from_database
from mytypes import GetAddressInput, GetAddressOutput, GetLastDataOutput

from fastapi import FastAPI, Response

from checker import get_address_data, AccountData_DTO

ELEMENTS_PER_PAGE = 10


@dataclass
class Error:
    message: str


async def check_address(input: GetAddressInput) -> GetAddressOutput:
    query_time: datetime = datetime.datetime.now()
    account_data: AccountData_DTO = get_address_data(input.address)
    add_to_database(query_time, account_data)
    result = GetAddressOutput(time=query_time, account_data=account_data)
    return result


async def get_data_from_page(
    page: int, response: Response
) -> GetLastDataOutput | Error:
    # render some html
    try:
        db_result = get_from_database(page)
    except IndexError as e:
        response.status_code = 500
        return Error(message=f"{e}")
    data: list[AccountData_DTO] = [
        AccountData_DTO(
            address=model.address,
            bandwidth=model.bandwidth,
            energy=model.energy,
            trx=model.trx,
        )
        for model in db_result.data
    ]
    result = GetLastDataOutput(pages=db_result.pages, page=db_result.page, data=data)
    return result


def main():
    app = FastAPI()

    app.post("/check_address")(check_address)  # info for address

    app.get("/get_page")(get_data_from_page)

    uvicorn.run(app)


if __name__ == "__main__":
    main()
