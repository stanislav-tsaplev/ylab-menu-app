from fastapi import FastAPI

from .database import create_db_and_tables
from .v1.routers import menu, submenu, dish
from .v1.endpoints import ENDPOINTS


app = FastAPI()


app.include_router(
    menu.router,
    prefix=ENDPOINTS["menus"],
    tags=["Menu"]
)
app.include_router(
    submenu.router,
    prefix=ENDPOINTS["submenus"],
    tags=["Submenu"]
)
app.include_router(
    dish.router,
    prefix=ENDPOINTS["dishes"],
    tags=["Dish"]
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
