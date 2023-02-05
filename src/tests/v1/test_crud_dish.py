from .conftest import app, pytest
from .resources.dish import (
    created_dish_data,
    creating_dish_data,
    deleted_dish_response,
    not_found_dish_response,
    read_dish_data,
    updated_dish_data,
    updating_dish_data,
)

pytestmark = pytest.mark.anyio


async def test_create_dish(client, existing_menu_id, existing_submenu_id):
    route_url = app.url_path_for(
        "create_dish", menu_id=existing_menu_id, submenu_id=existing_submenu_id
    )
    response = await client.post(url=route_url, json=creating_dish_data)

    assert response.status_code == 201

    response_json = response.json()
    assert response_json == {
        **created_dish_data,
        "id": response_json["id"],
    }


async def test_update_dish_success(
    client, existing_menu_id, existing_submenu_id, existing_dish_id
):
    route_url = app.url_path_for(
        "update_dish",
        menu_id=existing_menu_id,
        submenu_id=existing_submenu_id,
        dish_id=existing_dish_id,
    )
    response = await client.patch(url=route_url, json=updating_dish_data)

    assert response.status_code == 200
    assert response.json() == {
        **updated_dish_data,
        "id": existing_dish_id,
    }


async def test_update_dish_fail(
    client, existing_menu_id, existing_submenu_id, non_existing_dish_id
):
    route_url = app.url_path_for(
        "update_dish",
        menu_id=existing_menu_id,
        submenu_id=existing_submenu_id,
        dish_id=non_existing_dish_id,
    )
    response = await client.patch(url=route_url, json=updating_dish_data)

    assert response.status_code == 404
    assert response.json() == not_found_dish_response


async def test_delete_dish(
    client, existing_menu_id, existing_submenu_id, existing_dish_id
):
    route_url = app.url_path_for(
        "delete_dish",
        menu_id=existing_menu_id,
        submenu_id=existing_submenu_id,
        dish_id=existing_dish_id,
    )
    response = await client.delete(url=route_url)

    assert response.status_code == 200
    assert response.json() == deleted_dish_response


async def test_read_dish_success(
    client, existing_menu_id, existing_submenu_id, existing_dish_id
):
    route_url = app.url_path_for(
        "read_dish",
        menu_id=existing_menu_id,
        submenu_id=existing_submenu_id,
        dish_id=existing_dish_id,
    )
    response = await client.get(url=route_url)

    assert response.status_code == 200
    assert response.json() == {
        **read_dish_data,
        "id": existing_dish_id,
    }


async def test_read_dish_fail(
    client, existing_menu_id, existing_submenu_id, non_existing_dish_id
):
    route_url = app.url_path_for(
        "read_dish",
        menu_id=existing_menu_id,
        submenu_id=existing_submenu_id,
        dish_id=non_existing_dish_id,
    )
    response = await client.get(url=route_url)

    assert response.status_code == 404
    assert response.json() == not_found_dish_response


async def test_read_all_dishes(
    client, existing_menu_id, existing_submenu_id, existing_dish_id
):
    route_url = app.url_path_for(
        "read_all_dishes",
        menu_id=existing_menu_id,
        submenu_id=existing_submenu_id,
    )
    response = await client.get(url=route_url)

    assert response.status_code == 200
    assert response.json() == [
        {
            **read_dish_data,
            "id": existing_dish_id,
        }
    ]
