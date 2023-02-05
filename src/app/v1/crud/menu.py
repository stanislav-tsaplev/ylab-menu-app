from uuid import UUID

from .. import cache, db
from ..models.menu import MenuCreate, MenuCreated, MenuRead, MenuUpdate, MenuUpdated


async def create_menu(menu_creating_data: MenuCreate) -> MenuCreated:
    db_menu = await db.create_menu(menu_creating_data)
    # await cache.put_menu(db_menu)

    return db_menu


async def update_menu(
    menu_id: UUID, menu_updating_data: MenuUpdate
) -> MenuUpdated | None:
    db_menu = await db.update_menu(menu_id, menu_updating_data)
    if db_menu is None:
        return None

    await cache.delete_menu(menu_id)
    # await cache.put_menu(db_menu)

    return db_menu


async def delete_menu(menu_id: UUID) -> None:
    await db.delete_menu(menu_id)
    await cache.delete_menu(menu_id, cascade=True)


async def read_menu(menu_id: UUID) -> MenuRead | None:
    cached_menu = await cache.get_menu(menu_id)
    if cached_menu is not None:
        return cached_menu

    db_menu = await db.read_menu(menu_id)
    if db_menu is not None:
        await cache.put_menu(db_menu)
        return db_menu

    return None


async def read_all_menus() -> list[MenuRead]:
    return await db.read_all_menus()
