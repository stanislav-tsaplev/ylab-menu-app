from uuid import UUID

from fastapi import APIRouter, HTTPException

from .. import crud
from ..models.common import ResultInfo
from ..models.dish import (
    DishCreate,
    DishCreated,
    DishRead,
    DishUpdate,
    DishUpdated,
)
from .helpers import http_exception_response

router = APIRouter()


@router.post(
    "/",
    status_code=201,
    responses=http_exception_response(
        status_code=404, detail="submenu not found"
    ),
)
def create_dish(
    menu_id: UUID, submenu_id: UUID, dish: DishCreate
) -> DishCreated:
    created_dish = crud.create_dish(submenu_id, dish)
    if created_dish is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return created_dish


@router.patch(
    "/{dish_id}",
    responses=http_exception_response(
        status_code=404, detail="dish not found"
    ),
)
def update_dish(
    menu_id: UUID, submenu_id: UUID, dish_id: UUID, updated_dish: DishUpdate
) -> DishUpdated:
    dish = crud.update_dish(dish_id, updated_dish)
    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish


@router.delete("/{dish_id}")
def delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> ResultInfo:
    crud.delete_dish(dish_id)
    return ResultInfo(status=True, message="The dish has been deleted")


@router.get(
    "/{dish_id}",
    responses=http_exception_response(
        status_code=404, detail="dish not found"
    ),
)
def read_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> DishRead:
    dish = crud.read_dish(dish_id)
    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish


@router.get("/")
def read_all_dishes(menu_id: UUID, submenu_id: UUID) -> list[DishRead]:
    return crud.read_all_dishes(submenu_id)
