from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from app.database import db_engine
from app.main import app
from app.v1.routes import ROUTES

from .resources import creating_dish_data, creating_menu_data, creating_submenu_data

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(autouse=True)
def reset_database():
    SQLModel.metadata.drop_all(db_engine)
    SQLModel.metadata.create_all(db_engine)


@pytest.fixture(scope="session")
def client():
    test_client = TestClient(app, base_url=BASE_URL)
    yield test_client


@pytest.fixture
def created_menu(client):
    route_url = ROUTES["menus"]
    response = client.post(url=route_url, json=creating_menu_data)
    assert response.status_code == 201

    yield response.json()


@pytest.fixture
def created_submenu(client, created_menu):
    route_url = ROUTES["submenus"].format(menu_id=created_menu["id"])
    response = client.post(url=route_url, json=creating_submenu_data)
    assert response.status_code == 201

    yield {**response.json(), "menu_id": created_menu["id"]}


@pytest.fixture
def created_dish(client, created_submenu):
    route_url = ROUTES["dishes"].format(
        menu_id=created_submenu["menu_id"], submenu_id=created_submenu["id"]
    )
    response = client.post(url=route_url, json=creating_dish_data)
    assert response.status_code == 201

    yield response.json()


@pytest.fixture()
def existing_menu_id(created_menu):
    return created_menu["id"]


@pytest.fixture()
def existing_submenu_id(created_submenu):
    return created_submenu["id"]


@pytest.fixture()
def existing_dish_id(created_dish):
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
