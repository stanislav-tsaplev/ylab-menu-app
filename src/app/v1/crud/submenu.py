from uuid import UUID

from .. import cache, db
from ..models.submenu import (
    SubmenuCreate,
    SubmenuCreated,
    SubmenuRead,
    SubmenuUpdate,
    SubmenuUpdated,
)


def create_submenu(
    menu_id: UUID, submenu_creating_data: SubmenuCreate
) -> SubmenuCreated | None:
    db_submenu = db.create_submenu(menu_id, submenu_creating_data)
    # cache.put_submenu(db_submenu)

    return db_submenu


def update_submenu(
    submenu_id: UUID, submenu_updating_data: SubmenuUpdate
) -> SubmenuUpdated | None:
    db_submenu = db.update_submenu(submenu_id, submenu_updating_data)
    if db_submenu is None:
        return None

    assert db_submenu.menu_id
    cache.delete_submenu(db_submenu.menu_id, submenu_id)
    # cache.put_submenu(db_submenu)

    return db_submenu


def delete_submenu(menu_id: UUID, submenu_id: UUID) -> None:
    db.delete_submenu(submenu_id)

    cache.delete_menu(menu_id)
    cache.delete_submenu(menu_id, submenu_id, cascade=True)


def read_submenu(submenu_id: UUID) -> SubmenuRead | None:
    cached_submenu = cache.get_submenu(submenu_id)
    if cached_submenu is not None:
        return cached_submenu

    db_submenu = db.read_submenu(submenu_id)
    if db_submenu is not None:
        cache.put_submenu(db_submenu)
        return db_submenu

    return None


def read_all_submenus(menu_id: UUID) -> list[SubmenuRead]:
    return db.read_all_submenus(menu_id)
