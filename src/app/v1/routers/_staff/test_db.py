import yaml
from fastapi import APIRouter, status

from ... import crud
from ...models import MenuCreate, SubmenuCreate, DishCreate, ResultInfo

router = APIRouter(prefix="/api/v1")


@router.post("/test-db/", status_code=status.HTTP_201_CREATED)
@router.post("/test-db/{n}", status_code=status.HTTP_201_CREATED)
def create_test_db(n: int = 1) -> ResultInfo:
    with open(f"./app/v1/routers/_staff/test_db_{n}.yaml") as test_db_file:
        test_db_data = yaml.safe_load(test_db_file)

    for menu_data in test_db_data["menus"]:
        menu = crud.create_menu(
            MenuCreate(title=menu_data["title"], description=menu_data["desc"])
        )
        if menu is None:
            return ResultInfo(status=False, message="failure")

        for submenu_data in menu_data["submenus"]:
            submenu = crud.create_submenu(
                menu.id,
                SubmenuCreate(
                    title=submenu_data["title"], description=submenu_data["desc"]
                ),
            )
            if submenu is None:
                return ResultInfo(status=False, message="failure")

            for dish_data in submenu_data["dishes"]:
                dish = crud.create_dish(
                    submenu.id,
                    DishCreate.construct(
                        title=dish_data["title"],
                        description=dish_data["desc"],
                        price=dish_data["price"],
                    ),
                )
                if dish is None:
                    return ResultInfo(status=False, message="failure")

    return ResultInfo(status=True, message="success")


@router.delete("/test-db/")
def clear_db() -> ResultInfo:
    for menu in crud.read_all_menus():
        crud.delete_menu(menu.id)
    return ResultInfo(status=True, message="Database was successfully cleared")
