from uuid import UUID

from sqlmodel import Session, delete, select, update

from ...database import db_engine
from ..models.menu import Menu, MenuCreate, MenuUpdate


def create_menu(menu_creating_data: MenuCreate) -> Menu:
    """Creates a new menu with the `menu_creating_data` values.

    Returns newly created `Menu` object
    """
    with Session(db_engine) as session:
        db_menu = Menu.from_orm(menu_creating_data)
        session.add(db_menu)

        session.commit()
        session.refresh(db_menu)

        return db_menu


def update_menu(menu_id: UUID, menu_updating_data: MenuUpdate) -> Menu | None:
    """Updates the menu gotten by `menu_id`
    with the `menu_updating_data` values.

    Returns the updated `Menu` object,
    when `menu_id` is a valid menu id
    or `None` otherwise
    """
    with Session(db_engine) as session:
        db_menu = session.exec(
            select(Menu).where(Menu.id == menu_id)
        ).one_or_none()

        if db_menu is None:
            return None

        session.exec(
            update(Menu)
            .where(Menu.id == menu_id)
            .values(
                **menu_updating_data.dict(exclude={"id"}, exclude_unset=True)
            )
        )

        session.commit()
        session.refresh(db_menu)

        return db_menu


def delete_menu(menu_id: UUID) -> None:
    with Session(db_engine) as session:
        session.exec(delete(Menu).where(Menu.id == menu_id))

        session.commit()


def read_menu(menu_id: UUID) -> Menu | None:
    with Session(db_engine) as session:
        db_menu = session.get(Menu, menu_id)
        if db_menu is None:
            return None

        return db_menu


def read_all_menus() -> list[Menu]:
    with Session(db_engine) as session:
        db_menus = session.exec(select(Menu)).all()

        return db_menus
