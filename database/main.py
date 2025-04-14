from datetime import datetime

import dotenv
from sqlmodel import Session, select
from database.types import AccountData
from mytypes import AccountData_DTO

from . import engine

MAX_PER_PAGE = int(dotenv.get_key("config.env", "MAX_PER_PAGE"))


def get_records_count():
    with Session(engine) as session:
        stmt = select(AccountData)
        records = session.exec(stmt).all()
        return len(records)


def add_to_database(request_time: datetime, account_data: AccountData_DTO):
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


def get_from_database(page: int) -> list[AccountData]:
    with Session(engine) as session:
        pages = get_records_count() // MAX_PER_PAGE
        page = min(max(page - 1, 0), pages)
        offset = page * MAX_PER_PAGE

        stmt = (
            select(AccountData)
            .order_by(AccountData.request_datetime)
            .offset(offset)
            .limit(MAX_PER_PAGE)
        )
        return session.exec(stmt).all()
