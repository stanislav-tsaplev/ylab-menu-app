ROOT_PATH = "/api/v1"

ROUTE_PREFIXES = {
    "menus": ROOT_PATH + "/menus",
    "menu": ROOT_PATH + "/menus/{menu_id}",
    "submenus": ROOT_PATH + "/menus/{menu_id}/submenus",
    "submenu": ROOT_PATH + "/menus/{menu_id}/submenus/{submenu_id}",
    "dishes": ROOT_PATH + "/menus/{menu_id}/submenus/{submenu_id}/dishes",
    "dish": ROOT_PATH + "/menus/{menu_id}/submenus/{submenu_id}/dishes{dish_id}",
}
