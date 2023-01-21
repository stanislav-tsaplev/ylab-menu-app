import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app
from app.v1.crud.utils import clear_database
from app.endpoints import ROUTE_PREFIXES
from .resources import (
    creating_menu_data, creating_submenu_data, creating_dish_data
)


BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def client():
    cli = TestClient(
        app, 
        base_url=BASE_URL
    )
    yield cli


@pytest.fixture
def created_menu(client):
    route_url = ROUTE_PREFIXES["menus"]
    response = client.post(
        url=route_url,
        json=creating_menu_data
    )
    assert response.status_code == 201
    
    yield response.json()
    clear_database()


@pytest.fixture
def created_submenu(client, created_menu):
    route_url = ROUTE_PREFIXES["submenus"].format(
        menu_id=created_menu["id"]
    )
    response = client.post(
        url=route_url,
        json=creating_submenu_data
    )
    assert response.status_code == 201
    
    yield {
        **response.json(),
        "menu_id": created_menu["id"]
    }


@pytest.fixture
def created_dish(client, created_submenu):
    route_url = ROUTE_PREFIXES["dishes"].format(
        menu_id=created_submenu["menu_id"],
        submenu_id=created_submenu["id"]
    )
    response = client.post(
        url=route_url,
        json=creating_dish_data
    )
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
