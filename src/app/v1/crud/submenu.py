from uuid import UUID

from sqlmodel import Session, select, update, delete, func
from sqlalchemy.exc import IntegrityError

from ...database import engine
from ..models.submenu import Submenu, SubmenuCreate, SubmenuUpdate
from ..models import Dish


def create_submenu(menu_id: UUID, submenu: SubmenuCreate) -> Submenu | None:
    with Session(engine) as session:
        try:
            submenu.menu_id = menu_id
            db_submenu = Submenu.from_orm(submenu)
            session.add(db_submenu)

            session.commit()
        except IntegrityError as e:
            return None

        session.refresh(db_submenu)
        return db_submenu


def update_submenu(submenu_id: UUID, updated_submenu: SubmenuUpdate) -> Submenu | None:
    with Session(engine) as session:
        db_submenu = session.exec(
            select(Submenu)
            .where(Submenu.id == submenu_id)
        ).one_or_none()

        if db_submenu is None:
            return None

        session.exec(
            update(Submenu)
            .where(Submenu.id == submenu_id)
            .values(
                **updated_submenu.dict(
                    exclude={'id'},
                    exclude_unset=True
                )
            )
        )

        session.commit()
        session.refresh(db_submenu)

        return db_submenu


def delete_submenu(submenu_id: UUID) -> None:
    with Session(engine) as session:
        session.exec(
            delete(Submenu)
            .where(Submenu.id == submenu_id)
        )

        session.commit()


def read_submenu(submenu_id: UUID) -> Submenu | None:
    with Session(engine) as session:
        db_submenu = session.get(Submenu, submenu_id)
        if db_submenu is None:
            return None

        return db_submenu


def read_all_submenus(menu_id: UUID) -> list[Submenu]:
    with Session(engine) as session:
        db_submenus = session.exec(
            select(Submenu)
            .where(Submenu.menu_id == menu_id)
        ).all()

        return db_submenus
