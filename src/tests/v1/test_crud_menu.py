from .conftest import app, pytest
from .resources.menu import (
    created_menu_data,
    creating_menu_data,
    deleted_menu_response,
    not_found_menu_response,
    read_menu_data,
    updated_menu_data,
    updating_menu_data,
)

pytestmark = pytest.mark.anyio


async def test_create_menu(client):
    route_url = app.url_path_for("create_menu")
    response = await client.post(url=route_url, json=creating_menu_data)

    assert response.status_code == 201

    response_json = response.json()
    assert response_json == {
        **created_menu_data,
        "id": response_json["id"],
    }


async def test_update_menu_success(client, existing_menu_id):
    route_url = app.url_path_for("update_menu", menu_id=existing_menu_id)
    response = await client.patch(url=route_url, json=updating_menu_data)

    assert response.status_code == 200
    assert response.json() == {
        **updated_menu_data,
        "id": existing_menu_id,
    }


async def test_update_menu_fail(client, non_existing_menu_id):
    route_url = app.url_path_for("update_menu", menu_id=non_existing_menu_id)
    response = await client.patch(url=route_url, json=updating_menu_data)

    assert response.status_code == 404
    assert response.json() == not_found_menu_response


async def test_delete_menu(client, existing_menu_id):
    route_url = app.url_path_for("delete_menu", menu_id=existing_menu_id)
    response = await client.delete(url=route_url)

    assert response.status_code == 200
    assert response.json() == deleted_menu_response


async def test_read_menu_success(client, existing_menu_id):
    route_url = app.url_path_for("read_menu", menu_id=existing_menu_id)
    response = await client.get(url=route_url)

    assert response.status_code == 200
    assert response.json() == {
        **read_menu_data,
        "id": existing_menu_id,
    }


async def test_read_menu_fail(client, non_existing_menu_id):
    route_url = app.url_path_for("read_menu", menu_id=non_existing_menu_id)
    response = await client.get(url=route_url)

    assert response.status_code == 404
    assert response.json() == not_found_menu_response


async def test_read_all_menus(client, existing_menu_id):
    route_url = app.url_path_for("read_all_menus")
    response = await client.get(url=route_url)

    assert response.status_code == 200
    assert response.json() == [
        {
            **read_menu_data,
            "id": existing_menu_id,
        }
    ]
