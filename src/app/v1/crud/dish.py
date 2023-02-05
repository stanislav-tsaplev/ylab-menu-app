from uuid import UUID

from .. import cache, db
from ..models.dish import DishCreate, DishCreated, DishRead, DishUpdate, DishUpdated


async def create_dish(
    submenu_id: UUID, dish_creating_data: DishCreate
) -> DishCreated | None:
    db_dish = await db.create_dish(submenu_id, dish_creating_data)
    # await cache.put_dish(db_dish)

    return db_dish


async def update_dish(
    dish_id: UUID, dish_updating_data: DishUpdate
) -> DishUpdated | None:
    db_dish = await db.update_dish(dish_id, dish_updating_data)
    if db_dish is None:
        return None

    assert db_dish.submenu_id
    await cache.delete_dish(db_dish.submenu_id, dish_id)
    # await cache.put_dish(db_dish)

    return db_dish


async def delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> None:
    await db.delete_dish(dish_id)

    await cache.delete_menu(menu_id)
    await cache.delete_submenu(menu_id, submenu_id)
    await cache.delete_dish(submenu_id, dish_id)


async def read_dish(dish_id: UUID) -> DishRead | None:
    cached_dish = await cache.get_dish(dish_id)
    if cached_dish is not None:
        return cached_dish

    db_dish = await db.read_dish(dish_id)
    if db_dish is not None:
        await cache.put_dish(db_dish)
        return db_dish

    return None


async def read_all_dishes(submenu_id: UUID) -> list[DishRead]:
    return await db.read_all_dishes(submenu_id)
