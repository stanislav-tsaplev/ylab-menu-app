from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from .. import crud
from ..models.common import OperationResult
from ..models.menu import MenuCreate, MenuCreated, MenuRead, MenuUpdate, MenuUpdated
from .helpers import http_exception_response

router = APIRouter(prefix="/api/v1/menus")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_menu(menu_creating_data: MenuCreate) -> MenuCreated:
    created_menu = await crud.create_menu(menu_creating_data)
    return created_menu


@router.patch(
    "/{menu_id}",
    responses=http_exception_response(
        status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
    ),
)
async def update_menu(menu_id: UUID, menu_updating_data: MenuUpdate) -> MenuUpdated:
    updated_menu = await crud.update_menu(menu_id, menu_updating_data)
    if updated_menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
    return updated_menu


@router.delete("/{menu_id}")
async def delete_menu(menu_id: UUID) -> OperationResult:
    await crud.delete_menu(menu_id)
    return OperationResult(status=True, message="The menu has been deleted")


@router.get(
    "/{menu_id}",
    responses=http_exception_response(
        status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
    ),
)
async def read_menu(menu_id: UUID) -> MenuRead:
    menu = await crud.read_menu(menu_id)
    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
    return menu


@router.get("/")
async def read_all_menus() -> list[MenuRead]:
    all_menus = await crud.read_all_menus()
    return all_menus
