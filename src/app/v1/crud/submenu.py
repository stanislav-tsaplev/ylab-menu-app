from uuid import UUID

from .. import cache, db
from ..models.submenu import (
    SubmenuCreate,
    SubmenuCreated,
    SubmenuRead,
    SubmenuUpdate,
    SubmenuUpdated,
)


async def create_submenu(
    menu_id: UUID, submenu_creating_data: SubmenuCreate
) -> SubmenuCreated | None:
    db_submenu = await db.create_submenu(menu_id, submenu_creating_data)
    # await cache.put_submenu(db_submenu)

    return db_submenu


async def update_submenu(
    submenu_id: UUID, submenu_updating_data: SubmenuUpdate
) -> SubmenuUpdated | None:
    db_submenu = await db.update_submenu(submenu_id, submenu_updating_data)
    if db_submenu is None:
        return None

    assert db_submenu.menu_id
    await cache.delete_submenu(db_submenu.menu_id, submenu_id)
    # await cache.put_submenu(db_submenu)

    return db_submenu


async def delete_submenu(menu_id: UUID, submenu_id: UUID) -> None:
    await db.delete_submenu(submenu_id)

    await cache.delete_menu(menu_id)
    await cache.delete_submenu(menu_id, submenu_id, cascade=True)


async def read_submenu(submenu_id: UUID) -> SubmenuRead | None:
    cached_submenu = await cache.get_submenu(submenu_id)
    if cached_submenu is not None:
        return cached_submenu

    db_submenu = await db.read_submenu(submenu_id)
    if db_submenu is not None:
        await cache.put_submenu(db_submenu)
        return db_submenu

    return None


async def read_all_submenus(menu_id: UUID) -> list[SubmenuRead]:
    return await db.read_all_submenus(menu_id)
