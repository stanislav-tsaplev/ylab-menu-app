from dotenv import load_dotenv
from fastapi import FastAPI

from .database import create_db_and_tables
from .v1.routers import dish, menu, submenu
from .v1.routers._staff import test_db

load_dotenv()

app = FastAPI()

app.include_router(menu.router, tags=["menu"])
app.include_router(submenu.router, tags=["submenu"])
app.include_router(dish.router, tags=["dish"])

app.include_router(test_db.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
