from fastapi import FastAPI

from .database import create_db_and_tables
from .v1.routers import menu, submenu, dish


app = FastAPI()


app.include_router(
    menu.router,
    prefix="/api/v1/menus",
    tags=["menu"]
)
app.include_router(
    submenu.router,
    prefix="/api/v1/menus/{menu_id}/submenus",
    tags=["submenu"]
)
app.include_router(
    dish.router,
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["dish"]
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
