from uuid import UUID

from fastapi.encoders import jsonable_encoder

from ...cache import cache_engine
from ..models.submenu import Submenu

# Submenu objects are stored in Redis as a hash of its fields
# with hexified submenu id as key
# In addition special set stores submenu ids of a specific menu
# with hexified menu id prefixed by '~' symbol as key


async def put_submenu(submenu: Submenu) -> None:
    assert submenu.id and submenu.menu_id
    await cache_engine.hset(submenu.id.hex, mapping=jsonable_encoder(submenu))
    await cache_engine.sadd(f"~{submenu.menu_id.hex}", submenu.id.hex)


async def get_submenu(submenu_id: UUID) -> Submenu | None:
    submenu_dict = await cache_engine.get(submenu_id.hex)
    if submenu_dict is None:
        return None
    return Submenu.construct(**submenu_dict)


async def delete_submenu(
    menu_id: UUID, submenu_id: UUID, cascade: bool = False
) -> None:
    await cache_engine.delete(submenu_id.hex)
    await cache_engine.srem(f"~{menu_id.hex}", submenu_id.hex)

    if cascade:
        dish_id_hexes = await cache_engine.smembers(f"~{submenu_id.hex}")
        if dish_id_hexes:
            await cache_engine.delete(*dish_id_hexes)
        await cache_engine.delete(f"~{submenu_id.hex}")
