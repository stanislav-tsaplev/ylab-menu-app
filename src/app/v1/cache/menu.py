from uuid import UUID

from fastapi.encoders import jsonable_encoder

from ...cache import cache_engine
from ..models.menu import Menu


# Menu objects are stored in Redis as hash of its fields
# with hexified menu id as key


def put_menu(menu: Menu) -> None:
    cache_engine.hset(menu.id.hex, mapping=jsonable_encoder(menu))


def get_menu(menu_id: UUID) -> Menu | None:
    menu_dict = cache_engine.get(menu_id.hex)
    if menu_dict is None:
        return None
    return Menu.construct(**menu_dict)


def delete_menu(menu_id: UUID, cascade: bool = False) -> None:
    cache_engine.delete(menu_id.hex)

    if cascade:
        submenu_id_hexes = cache_engine.smembers(f"~{menu_id.hex}")
        for submenu_id_hex in submenu_id_hexes:
            dish_id_hexes = cache_engine.smembers(f"~{submenu_id_hex}")
            if dish_id_hexes:
                cache_engine.delete(*dish_id_hexes)
            cache_engine.delete(f"~{submenu_id_hex}")

        if submenu_id_hexes:
            cache_engine.delete(*submenu_id_hexes)
        cache_engine.delete(f"~{menu_id.hex}")
