from sqlmodel import Session, delete

from ...database import engine
from ..models.menu import Menu


def truncate_database() -> None:
    with Session(engine) as session:
        session.exec(delete(Menu))
        session.commit()