from uuid import UUID

from fastapi import APIRouter, HTTPException

from ..models.menu import (
    MenuCreate, MenuUpdate, MenuRead,
    MenuCreated, MenuUpdated
)
from .. import crud


router = APIRouter()


@router.post("/", status_code=201)
def create_menu(menu: MenuCreate) -> MenuCreated:
    return crud.create_menu(menu)


@router.patch("/{menu_id}")
def update_menu(menu_id: UUID, updated_menu: MenuUpdate) -> MenuUpdated:
    menu = crud.update_menu(menu_id, updated_menu)
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


@router.delete("/{menu_id}")
def delete_menu(menu_id: UUID) -> dict:
    crud.delete_menu(menu_id)
    return {
        "status": True, 
        "message": "The menu has been deleted"
    }


@router.get("/{menu_id}")
def read_menu(menu_id: UUID) -> MenuRead:
    menu = crud.read_menu(menu_id)
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    submenus_count = crud.menu.get_submenus_count(menu_id)
    dishes_count = crud.menu.get_total_dishes_count(menu_id)

    return MenuRead.construct(
        submenus_count=submenus_count,
        dishes_count=dishes_count,
        **menu.dict()
    )


@router.get("/", response_model=list[MenuRead])
def read_all_menus():
    return crud.read_all_menus()
