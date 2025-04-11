import uvicorn
from mytypes import Data_DTO, GetAddressInput, GetAddressOutput, GetLastDataOutput

from fastapi import FastAPI

ELEMENTS_PER_PAGE = 10


def main():
    app = FastAPI()

    @app.post("/check_address")  # info for address
    async def check_address(input: GetAddressInput) -> GetAddressOutput:
        result: GetAddressOutput = GetAddressOutput.model_validate(
            {"address": "0.0", "bandwidth": 0.0, "energy": 0.0, "trx": 0.0}
        )
        return result

    @app.get("/get_last")
    async def get_last_data(page: int) -> GetLastDataOutput:
        # render some html
        result = GetLastDataOutput.model_validate(
            {
                "page": page,
                "data": [
                    Data_DTO.model_validate(
                        {"address": f"{x}", "bandwidth": x, "energy": x, "trx": x}
                    )
                    for x in range(
                        page * ELEMENTS_PER_PAGE,
                        page * ELEMENTS_PER_PAGE + ELEMENTS_PER_PAGE,
                    )
                ],
            }
        )
        return result

    uvicorn.run(app)


if __name__ == "__main__":
    main()
