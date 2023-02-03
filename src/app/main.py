from dotenv import load_dotenv
from fastapi import FastAPI

from .database import create_db_and_tables
from .v1._staff import _test_db
from .v1.routers import menu, submenu, dish

load_dotenv()

app = FastAPI()

app.include_router(menu.router, tags=["menu"])
app.include_router(submenu.router, tags=["submenu"])
app.include_router(dish.router, tags=["dish"])

app.include_router(_test_db.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
