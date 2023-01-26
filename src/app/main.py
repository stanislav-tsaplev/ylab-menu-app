from fastapi import FastAPI

from .database import create_db_and_tables
from .v1.routers import menu, submenu, dish
from .v1.routes import ROUTES


app = FastAPI()


app.include_router(
    menu.router,
    prefix=ROUTES["menus"],
    tags=["menu"]
)
app.include_router(
    submenu.router,
    prefix=ROUTES["submenus"],
    tags=["submenu"]
)
app.include_router(
    dish.router,
    prefix=ROUTES["dishes"],
    tags=["dish"]
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
