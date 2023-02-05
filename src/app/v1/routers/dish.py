from uuid import UUID

from fastapi import APIRouter, HTTPException

from .. import crud
from ..models.common import OperationResult
from ..models.dish import DishCreate, DishCreated, DishRead, DishUpdate, DishUpdated
from .helpers import http_exception_response

router = APIRouter(prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")


@router.post(
    "/",
    status_code=201,
    responses=http_exception_response(status_code=404, detail="submenu not found"),
)
async def create_dish(
    menu_id: UUID, submenu_id: UUID, dish_creating_data: DishCreate
) -> DishCreated:
    created_dish = await crud.create_dish(submenu_id, dish_creating_data)
    if created_dish is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return created_dish


@router.patch(
    "/{dish_id}",
    responses=http_exception_response(status_code=404, detail="dish not found"),
)
async def update_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish_updating_data: DishUpdate,
) -> DishUpdated:
    updated_dish = await crud.update_dish(dish_id, dish_updating_data)
    if updated_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return updated_dish


@router.delete("/{dish_id}")
async def delete_dish(
    menu_id: UUID, submenu_id: UUID, dish_id: UUID
) -> OperationResult:
    await crud.delete_dish(menu_id, submenu_id, dish_id)
    return OperationResult(status=True, message="The dish has been deleted")


@router.get(
    "/{dish_id}",
    responses=http_exception_response(status_code=404, detail="dish not found"),
)
async def read_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> DishRead:
    dish = await crud.read_dish(dish_id)
    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish


@router.get("/")
async def read_all_dishes(menu_id: UUID, submenu_id: UUID) -> list[DishRead]:
    return await crud.read_all_dishes(submenu_id)
