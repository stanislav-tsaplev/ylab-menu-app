from uuid import UUID

from .. import db, cache
from ..models.menu import (
    MenuCreate,
    MenuCreated,
    MenuRead,
    MenuUpdate,
    MenuUpdated,
)


def create_menu(menu_creating_data: MenuCreate) -> MenuCreated:
    db_menu = db.create_menu(menu_creating_data)
    # cache.put_menu(db_menu)

    return db_menu


def update_menu(
    menu_id: UUID, menu_updating_data: MenuUpdate
) -> MenuUpdated | None:
    db_menu = db.update_menu(menu_id, menu_updating_data)
    if db_menu is None:
        return None

    cache.delete_menu(menu_id)
    # cache.put_menu(db_menu)

    return db_menu


def delete_menu(menu_id: UUID) -> None:
    db.delete_menu(menu_id)
    cache.delete_menu(menu_id, cascade=True)


def read_menu(menu_id: UUID) -> MenuRead | None:
    cached_menu = cache.get_menu(menu_id)
    if cached_menu is not None:
        return cached_menu

    db_menu = db.read_menu(menu_id)
    if db_menu is not None:
        cache.put_menu(db_menu)
        return db_menu

    return None


def read_all_menus() -> list[MenuRead]:
    return db.read_all_menus()
