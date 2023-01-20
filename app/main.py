from fastapi import FastAPI

from .database import create_db_and_tables
from .v1.routers import menu, submenu, dish
from .endpoints import ROUTE_PREFIXES


app = FastAPI()


app.include_router(
    menu.router,
    prefix=ROUTE_PREFIXES["menu"],
    tags=["menu"]
)
app.include_router(
    submenu.router,
    prefix=ROUTE_PREFIXES["submenu"],
    tags=["submenu"]
)
app.include_router(
    dish.router,
    prefix=ROUTE_PREFIXES["dish"],
    tags=["dish"]
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
