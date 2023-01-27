from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from .. import crud
from ..models.common import ResultInfo
from ..models.submenu import (
    SubmenuCreate,
    SubmenuCreated,
    SubmenuRead,
    SubmenuUpdate,
    SubmenuUpdated,
)
from .helpers import http_exception_response

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses=http_exception_response(
        status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
    ),
)
def create_submenu(menu_id: UUID, submenu: SubmenuCreate) -> SubmenuCreated:
    created_submenu = crud.create_submenu(menu_id, submenu)
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
def update_submenu(
    menu_id: UUID, submenu_id: UUID, updated_submenu: SubmenuUpdate
) -> SubmenuUpdated:
    submenu = crud.update_submenu(submenu_id, updated_submenu)
    if submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    return submenu


@router.delete("/{submenu_id}")
def delete_submenu(menu_id: UUID, submenu_id: UUID) -> ResultInfo:
    crud.delete_submenu(submenu_id)
    return ResultInfo(status=True, message="The submenu has been deleted")


@router.get(
    "/{submenu_id}",
    responses=http_exception_response(
        status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
    ),
)
def read_submenu(menu_id: UUID, submenu_id: UUID) -> SubmenuRead:
    submenu = crud.read_submenu(submenu_id)
    if submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    return submenu


@router.get("/")
def read_all_submenus(menu_id: UUID) -> list[SubmenuRead]:
    return crud.read_all_submenus(menu_id)
