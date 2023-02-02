from uuid import UUID

from fastapi.encoders import jsonable_encoder

from ...cache import cache_engine
from ..models.dish import Dish

# Dish objects are stored in Redis as a hash of its fields
# with hexified dish id as key
# In addition special set stores dish ids of a specific submenu
# with hexified submenu id prefixed by '~' symbol as key


def put_dish(dish: Dish) -> None:
    assert dish.id and dish.submenu_id
    cache_engine.hset(dish.id.hex, mapping=jsonable_encoder(dish))
    cache_engine.sadd(f"~{dish.submenu_id.hex}", dish.id.hex)


def get_dish(dish_id: UUID) -> Dish | None:
    dish_dict = cache_engine.get(dish_id.hex)
    if dish_dict is None:
        return None
    return Dish.construct(**dish_dict)


def delete_dish(submenu_id: UUID, dish_id: UUID) -> None:
    cache_engine.delete(dish_id.hex)
    cache_engine.srem(f"~{submenu_id.hex}", dish_id.hex)
