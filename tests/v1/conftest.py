import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app
from app.v1.crud.utils import truncate_database
from app.endpoints import ROOT_PATH, ROUTE_PREFIXES
from .resources import creating_menu_data


BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def client():
    cli = TestClient(
        app, 
        base_url=BASE_URL,
        root_path=ROOT_PATH
    )
    yield cli


@pytest.fixture
def created_menu(client):
    route_url = ROUTE_PREFIXES["menu"] + "/"
    response = client.post(
        url=route_url,
        json=creating_menu_data
    )
    assert response.status_code == 201
    
    yield response.json()
    truncate_database()


@pytest.fixture()
def existing_menu_id(created_menu):
    return created_menu["id"]


@pytest.fixture()
def non_existing_menu_id():
    return uuid4()
