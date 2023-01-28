from uuid import UUID

from ...cache import dish_storage
from ..models.dish import Dish


def put_dish(dish: Dish) -> None:
    dish_storage[dish.id.hex] = dish


def get_dish(dish_id: UUID) -> Dish:
    return dish_storage.get(dish_id.hex)


def delete_dish(dish_id: UUID) -> None:
    dish_storage.pop(dish_id.hex, None)


def delete_all_dishes() -> None:
    dish_storage.clear()
