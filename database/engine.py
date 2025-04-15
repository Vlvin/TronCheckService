from dotenv import get_key
from sqlalchemy import Engine
from sqlmodel import create_engine


CONNECTION_STRING: str = get_key(".env", "CONNECTION_STRING")
# print(CONNECTION_STRING)
engine: Engine = create_engine(CONNECTION_STRING)
# SQLModel.metadata.create_all(engine)
