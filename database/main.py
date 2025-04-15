from datetime import datetime
from math import ceil

import dotenv
from sqlmodel import Session, select
from .models import AccountData
from .types import GetFromDatabaseOutput
from mytypes import AccountData_DTO

from . import engine

MAX_PER_PAGE = int(dotenv.get_key("config.env", "MAX_PER_PAGE"))


def get_records_count() -> int:
    with Session(engine) as session:
        stmt = select(AccountData)
        records = session.exec(stmt).all()
        return len(records)


def add_to_database(request_time: datetime, account_data: AccountData_DTO) -> None:
    with Session(engine) as session:
        new_data = AccountData(
            request_datetime=request_time,
            address=account_data.address,
            bandwidth=account_data.bandwidth,
            energy=account_data.energy,
            trx=account_data.trx,
        )
        session.add(new_data)
        session.commit()


def get_from_database(page: int) -> GetFromDatabaseOutput:
    with Session(engine) as session:
        pages = ceil(get_records_count() / MAX_PER_PAGE)
        if 0 > page or page >= pages:
            raise IndexError(f"expected page 0-{pages}, got {page}")
        offset = page * MAX_PER_PAGE

        stmt = (
            select(AccountData)
            .order_by(AccountData.request_datetime)
            .offset(offset)
            .limit(MAX_PER_PAGE)
        )
        result = GetFromDatabaseOutput(
            pages=pages, page=page, data=session.exec(stmt).all()
        )
        return result
