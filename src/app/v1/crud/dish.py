from uuid import UUID

from .. import db, cache
from ..models.dish import (
    DishCreate,
    DishCreated,
    DishRead,
    DishUpdate,
    DishUpdated,
)


def create_dish(
    submenu_id: UUID, dish_creating_data: DishCreate
) -> DishCreated | None:
    db_dish = db.create_dish(submenu_id, dish_creating_data)
    # cache.put_dish(db_dish)

    return db_dish


def update_dish(
    dish_id: UUID, dish_updating_data: DishUpdate
) -> DishUpdated | None:
    db_dish = db.update_dish(dish_id, dish_updating_data)
    if db_dish is None:
        return None

    cache.delete_dish(dish_id)
    # cache.put_dish(db_dish)

    return db_dish


def delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> None:
    db.delete_dish(dish_id)

    cache.delete_menu(menu_id)
    cache.delete_submenu(submenu_id)
    cache.delete_dish(dish_id)


def read_dish(dish_id: UUID) -> DishRead | None:
    cached_dish = cache.get_dish(dish_id)
    if cached_dish is not None:
        return cached_dish

    db_dish = db.read_dish(dish_id)
    if db_dish is not None:
        cache.put_dish(db_dish)
        return db_dish

    return None


def read_all_dishes(submenu_id: UUID) -> list[DishRead]:
    return db.read_all_dishes(submenu_id)
