from .conftest import app, pytest
from .resources.submenu import (
    created_submenu_data,
    creating_submenu_data,
    deleted_submenu_response,
    not_found_submenu_response,
    read_submenu_data,
    updated_submenu_data,
    updating_submenu_data,
)

pytestmark = pytest.mark.anyio


async def test_create_submenu(client, existing_menu_id):
    route_url = app.url_path_for("create_submenu", menu_id=existing_menu_id)
    response = await client.post(url=route_url, json=creating_submenu_data)

    assert response.status_code == 201

    response_json = response.json()
    assert response_json == {
        **created_submenu_data,
        "id": response_json["id"],
    }


async def test_update_submenu_success(client, existing_menu_id, existing_submenu_id):
    route_url = app.url_path_for(
        "update_submenu", menu_id=existing_menu_id, submenu_id=existing_submenu_id
    )
    response = await client.patch(url=route_url, json=updating_submenu_data)

    assert response.status_code == 200
    assert response.json() == {
        **updated_submenu_data,
        "id": existing_submenu_id,
    }


async def test_update_submenu_fail(client, existing_menu_id, non_existing_submenu_id):
    route_url = app.url_path_for(
        "update_submenu", menu_id=existing_menu_id, submenu_id=non_existing_submenu_id
    )
    response = await client.patch(url=route_url, json=updating_submenu_data)

    assert response.status_code == 404
    assert response.json() == not_found_submenu_response


async def test_delete_submenu(client, existing_menu_id, existing_submenu_id):
    route_url = app.url_path_for(
        "delete_submenu", menu_id=existing_menu_id, submenu_id=existing_submenu_id
    )
    response = await client.delete(url=route_url)

    assert response.status_code == 200
    assert response.json() == deleted_submenu_response


async def test_read_submenu_success(client, existing_menu_id, existing_submenu_id):
    route_url = app.url_path_for(
        "read_submenu", menu_id=existing_menu_id, submenu_id=existing_submenu_id
    )
    response = await client.get(url=route_url)

    assert response.status_code == 200
    assert response.json() == {
        **read_submenu_data,
        "id": existing_submenu_id,
    }


async def test_read_submenu_fail(client, existing_menu_id, non_existing_submenu_id):
    route_url = app.url_path_for(
        "read_submenu", menu_id=existing_menu_id, submenu_id=non_existing_submenu_id
    )
    response = await client.get(url=route_url)

    assert response.status_code == 404
    assert response.json() == not_found_submenu_response


async def test_read_all_submenus(client, existing_menu_id, existing_submenu_id):
    route_url = app.url_path_for("read_all_submenus", menu_id=existing_menu_id)
    response = await client.get(url=route_url)

    assert response.status_code == 200
    assert response.json() == [
        {
            **read_submenu_data,
            "id": existing_submenu_id,
        }
    ]
