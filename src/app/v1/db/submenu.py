from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, delete, select, update

from ...database import db_engine
from ..models.submenu import Submenu, SubmenuCreate, SubmenuUpdate


def create_submenu(
    menu_id: UUID, submenu_creating_data: SubmenuCreate
) -> Submenu | None:
    with Session(db_engine) as session:
        try:
            submenu_creating_data.menu_id = menu_id
            db_submenu = Submenu.from_orm(submenu_creating_data)
            session.add(db_submenu)

            session.commit()
        except IntegrityError:
            return None

        session.refresh(db_submenu)
        return db_submenu


def update_submenu(
    submenu_id: UUID, submenu_updating_data: SubmenuUpdate
) -> Submenu | None:
    with Session(db_engine) as session:
        db_submenu = session.exec(
            select(Submenu).where(Submenu.id == submenu_id)
        ).one_or_none()

        if db_submenu is None:
            return None

        session.exec(
            update(Submenu)
            .where(Submenu.id == submenu_id)
            .values(**submenu_updating_data.dict(exclude={"id"}, exclude_unset=True))
        )

        session.commit()
        session.refresh(db_submenu)

        return db_submenu


def delete_submenu(submenu_id: UUID) -> None:
    with Session(db_engine) as session:
        session.exec(delete(Submenu).where(Submenu.id == submenu_id))

        session.commit()


def read_submenu(submenu_id: UUID) -> Submenu | None:
    with Session(db_engine) as session:
        db_submenu = session.get(Submenu, submenu_id)
        if db_submenu is None:
            return None

        return db_submenu


def read_all_submenus(menu_id: UUID) -> list[Submenu]:
    with Session(db_engine) as session:
        db_submenus = session.exec(
            select(Submenu).where(Submenu.menu_id == menu_id)
        ).all()

        return db_submenus
