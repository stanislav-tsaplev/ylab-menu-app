import yaml
from fastapi import APIRouter, status

from .. import crud
from ..models import MenuCreate, SubmenuCreate, DishCreate, OperationResult

router = APIRouter(prefix="/api/v1")


@router.post("/test-db/", status_code=status.HTTP_201_CREATED)
@router.post("/test-db/{n}", status_code=status.HTTP_201_CREATED)
def create_test_db(n: int = 1) -> OperationResult:
    with open(f"/app/v1/_staff/test_db_{n}.yaml") as test_db_file:
        test_db_data = yaml.safe_load(test_db_file)

    for menu_data in test_db_data["menus"]:
        menu = crud.create_menu(
            MenuCreate(title=menu_data["title"], description=menu_data["description"])
        )
        if menu is None:
            return OperationResult(status=False, message="Test data loading failed")

        for submenu_data in menu_data["submenus"]:
            submenu = crud.create_submenu(
                menu.id,
                SubmenuCreate(
                    title=submenu_data["title"], description=submenu_data["description"]
                ),
            )
            if submenu is None:
                return OperationResult(status=False, message="Test data loading failed")

            for dish_data in submenu_data["dishes"]:
                dish = crud.create_dish(
                    submenu.id,
                    DishCreate.construct(
                        title=dish_data["title"],
                        description=dish_data["description"],
                        price=dish_data["price"],
                    ),
                )
                if dish is None:
                    return OperationResult(
                        status=False, message="Test data loading failed"
                    )

    return OperationResult(status=True, message="Test data was successfully loaded")


@router.delete("/test-db/")
def clear_test_db() -> OperationResult:
    for menu in crud.read_all_menus():
        crud.delete_menu(menu.id)
    return OperationResult(status=True, message="Database was successfully cleared")
