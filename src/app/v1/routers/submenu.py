from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from .. import crud
from ..models.common import OperationResult
from ..models.submenu import (
    SubmenuCreate,
    SubmenuCreated,
    SubmenuRead,
    SubmenuUpdate,
    SubmenuUpdated,
)
from .helpers import http_exception_response

router = APIRouter(prefix="/api/v1/menus/{menu_id}/submenus")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses=http_exception_response(
        status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
    ),
)
async def create_submenu(
    menu_id: UUID, submenu_creating_data: SubmenuCreate
) -> SubmenuCreated:
    created_submenu = await crud.create_submenu(menu_id, submenu_creating_data)
    if created_submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
    return created_submenu


@router.patch(
    "/{submenu_id}",
    responses=http_exception_response(
        status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
    ),
)
async def update_submenu(
    menu_id: UUID, submenu_id: UUID, submenu_updating_data: SubmenuUpdate
) -> SubmenuUpdated:
    updated_submenu = await crud.update_submenu(submenu_id, submenu_updating_data)
    if updated_submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    return updated_submenu


@router.delete("/{submenu_id}")
async def delete_submenu(menu_id: UUID, submenu_id: UUID) -> OperationResult:
    await crud.delete_submenu(menu_id, submenu_id)
    return OperationResult(status=True, message="The submenu has been deleted")


@router.get(
    "/{submenu_id}",
    responses=http_exception_response(
        status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
    ),
)
async def read_submenu(menu_id: UUID, submenu_id: UUID) -> SubmenuRead:
    submenu = await crud.read_submenu(submenu_id)
    if submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    return submenu


@router.get("/")
async def read_all_submenus(menu_id: UUID) -> list[SubmenuRead]:
    return await crud.read_all_submenus(menu_id)
