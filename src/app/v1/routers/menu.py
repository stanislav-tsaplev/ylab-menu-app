from uuid import UUID

from fastapi import APIRouter, HTTPException

from ..models.menu import (
    MenuCreate, MenuUpdate, MenuRead,
    MenuCreated, MenuUpdated
)
from ..models.common import ResultInfo
from .. import crud
from .helpers import http_exception_response


router = APIRouter()


@router.post("/", status_code=201)
def create_menu(menu: MenuCreate) -> MenuCreated:
    return crud.create_menu(menu)


@router.patch("/{menu_id}",
    responses=http_exception_response(status_code=404, detail="menu not found")
)
def update_menu(menu_id: UUID, updated_menu: MenuUpdate) -> MenuUpdated:
    menu = crud.update_menu(menu_id, updated_menu)
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


@router.delete("/{menu_id}")
def delete_menu(menu_id: UUID) -> ResultInfo:
    crud.delete_menu(menu_id)
    return ResultInfo(
        status=True,
        message="The menu has been deleted"
    )


@router.get("/{menu_id}",
    responses=http_exception_response(status_code=404, detail="menu not found")
)
def read_menu(menu_id: UUID) -> MenuRead:
    menu = crud.read_menu(menu_id)
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


@router.get("/", response_model=list[MenuRead])
def read_all_menus():
    return crud.read_all_menus()
