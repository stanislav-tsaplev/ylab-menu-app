import yaml
from fastapi import APIRouter, status

from ....app.v1 import crud
from ....app.v1.models import MenuCreate, SubmenuCreate, DishCreate, OperationResult

router = APIRouter(prefix="/_srv/v1")


@router.post("/data/test/", status_code=status.HTTP_201_CREATED)
@router.post("/data/test/{n}", status_code=status.HTTP_201_CREATED)
async def create_test_dataset(n: int = 1) -> OperationResult:
    with open(f"src/service/v1/resources/test_dataset_{n}.yaml") as test_dataset_file:
        test_dataset_data = yaml.safe_load(test_dataset_file)

    for menu_data in test_dataset_data["menus"]:
        menu = await crud.create_menu(
            MenuCreate(title=menu_data["title"], description=menu_data["description"])
        )
        if menu is None:
            return OperationResult(status=False, message="Test data loading failed")

        for submenu_data in menu_data["submenus"]:
            submenu = await crud.create_submenu(
                menu.id,
                SubmenuCreate(
                    title=submenu_data["title"], description=submenu_data["description"]
                ),
            )
            if submenu is None:
                return OperationResult(status=False, message="Test data loading failed")

            for dish_data in submenu_data["dishes"]:
                dish = await crud.create_dish(
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


@router.delete("/data/")
async def clear_test_db() -> OperationResult:
    all_menus = await crud.read_all_menus()
    for menu in all_menus:
        await crud.delete_menu(menu.id)
    return OperationResult(status=True, message="Database was successfully cleared")
