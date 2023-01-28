from uuid import UUID

from ...cache import menu_storage
from ..models.menu import Menu


def put_menu(menu: Menu) -> None:
    menu_storage[menu.id.hex] = menu


def get_menu(menu_id: UUID) -> Menu:
    return menu_storage.get(menu_id.hex)


def delete_menu(menu_id: UUID) -> None:
    menu_storage.pop(menu_id.hex, None)


def delete_all_menus() -> None:
    menu_storage.clear()
