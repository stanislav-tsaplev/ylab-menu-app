from dotenv import load_dotenv
from fastapi import FastAPI

from .database import init_db
from .v1._srv import _db_data
from .v1.routers import menu, submenu, dish, catalog

load_dotenv()

app = FastAPI()

app.include_router(menu.router, tags=["menu"])
app.include_router(submenu.router, tags=["submenu"])
app.include_router(dish.router, tags=["dish"])
app.include_router(catalog.router, tags=["catalog"])

app.include_router(_db_data.router, include_in_schema=False)


@app.on_event("startup")
async def on_startup():
    await init_db()
