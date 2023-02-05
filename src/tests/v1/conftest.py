from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel

from app.database import db_engine
from app.main import app

from .resources import creating_dish_data, creating_menu_data, creating_submenu_data

pytestmark = pytest.mark.anyio

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
async def reset_database(anyio_backend):
    async with db_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


@pytest.fixture(scope="session")
async def client(anyio_backend):
    async with AsyncClient(app=app, base_url=BASE_URL) as test_client:
        yield test_client


@pytest.fixture
async def created_menu(client: AsyncClient):
    route_url = app.url_path_for("create_menu")
    response = await client.post(url=route_url, json=creating_menu_data)
    assert response.status_code == 201

    return response.json()


@pytest.fixture
async def created_submenu(client: AsyncClient, created_menu: dict):
    route_url = app.url_path_for("create_submenu", menu_id=created_menu["id"])
    response = await client.post(url=route_url, json=creating_submenu_data)
    assert response.status_code == 201

    return {**response.json(), "menu_id": created_menu["id"]}


@pytest.fixture
async def created_dish(client: AsyncClient, created_submenu: dict):
    route_url = app.url_path_for(
        "create_dish",
        menu_id=created_submenu["menu_id"],
        submenu_id=created_submenu["id"],
    )
    response = await client.post(url=route_url, json=creating_dish_data)
    assert response.status_code == 201

    yield response.json()


@pytest.fixture()
def existing_menu_id(created_menu: dict):
    return created_menu["id"]


@pytest.fixture()
def existing_submenu_id(created_submenu: dict):
    return created_submenu["id"]


@pytest.fixture()
def existing_dish_id(created_dish: dict):
    return created_dish["id"]


@pytest.fixture()
def non_existing_menu_id():
    return uuid4()


@pytest.fixture()
def non_existing_submenu_id():
    return uuid4()


@pytest.fixture()
def non_existing_dish_id():
    return uuid4()
