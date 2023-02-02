from os import environ as env

from sqlmodel import SQLModel, create_engine

DB_USER = env["DB_USER"]
DB_PASS = env["DB_PASS"]
DB_HOST = env["DB_HOST"]
DB_NAME = env["DB_NAME"]

DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"


db_engine = create_engine(DB_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(db_engine)
