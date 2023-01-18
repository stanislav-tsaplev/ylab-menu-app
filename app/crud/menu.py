from uuid import UUID

from sqlmodel import Session, select, update, delete, func

from ..database import engine
from ..models.menu import Menu, MenuCreate, MenuUpdate
from ..models import Submenu, Dish


def create_menu(menu: MenuCreate) -> Menu:
    with Session(engine) as session:
        db_menu = Menu.from_orm(menu)
        session.add(db_menu)

        session.commit()
        session.refresh(db_menu)

        return db_menu


def update_menu(menu_id: UUID, updated_menu: MenuUpdate) -> Menu | None:
    with Session(engine) as session:
        db_menu = session.exec(
            select(Menu)
            .where(Menu.id == menu_id)
        ).one_or_none()

        if db_menu is None:
            return None

        session.exec(
            update(Menu)
            .where(Menu.id == menu_id)
            .values(
                **updated_menu.dict(
                    exclude={'id'},
                    exclude_unset=True
                )
            )
        )

        session.commit()
        session.refresh(db_menu)

        return db_menu


def delete_menu(menu_id: UUID) -> None:
    with Session(engine) as session:
        session.exec(
            delete(Menu)
            .where(Menu.id == menu_id)
        )

        session.commit()


def read_menu(menu_id: UUID) -> Menu | None:
    with Session(engine) as session:
        db_menu = session.get(Menu, menu_id)
        if db_menu is None:
            return None

        return db_menu


def read_all_menus() -> list[Menu]:
    with Session(engine) as session:
        db_menus = session.exec(
            select(Menu)
        ).all()

        return db_menus


def get_submenus_count(menu_id: UUID) -> int:
    with Session(engine) as session:
        submenus_count = session.exec(
            select(func.count(Submenu.id))
            .where(Submenu.menu_id == menu_id)
        ).one()

        return submenus_count


def get_total_dishes_count(menu_id: UUID) -> int:
    with Session(engine) as session:
        dishes_count = session.exec(
            select(func.count(Dish.id))
            .join(Submenu)
            .where(Dish.submenu_id == Submenu.id and Submenu.menu_id == menu_id)
        ).one()

        return dishes_count
