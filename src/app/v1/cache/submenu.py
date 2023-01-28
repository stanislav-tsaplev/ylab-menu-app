from uuid import UUID

from ...cache import submenu_storage
from ..models.submenu import Submenu


def put_submenu(submenu: Submenu) -> None:
    submenu_storage[submenu.id.hex] = submenu


def get_submenu(submenu_id: UUID) -> Submenu:
    return submenu_storage.get(submenu_id.hex)


def delete_submenu(submenu_id: UUID) -> None:
    submenu_storage.pop(submenu_id.hex, None)


def delete_all_submenus() -> None:
    submenu_storage.clear()
