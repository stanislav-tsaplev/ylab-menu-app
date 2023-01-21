from app.endpoints import ROUTE_PREFIXES
from .resources.submenu import (
    creating_submenu_data, updating_submenu_data,
    created_submenu_data, updated_submenu_data, read_submenu_data, 
    deleted_submenu_response, not_found_submenu_response
)


def test_create_submenu(client, existing_menu_id):
    route_url = ROUTE_PREFIXES["submenus"].format(
        menu_id=existing_menu_id
    )
    response = client.post(
        url=route_url, 
        json=creating_submenu_data
    )

    assert response.status_code == 201

    response_json = response.json()
    assert response_json == {
        **created_submenu_data,
        "id": response_json["id"],
    }


def test_update_submenu_success(client, existing_menu_id, existing_submenu_id):
    route_url = ROUTE_PREFIXES["submenu"].format(
        menu_id=existing_menu_id,
        submenu_id=existing_submenu_id
    )
    response = client.patch(
        url=route_url, 
        json=updating_submenu_data
    )

    assert response.status_code == 200
    assert response.json() == {
        **updated_submenu_data,
        "id": existing_submenu_id,
    }


def test_update_submenu_fail(client, existing_menu_id, non_existing_submenu_id):
    route_url = ROUTE_PREFIXES["submenu"].format(
        menu_id=existing_menu_id,
        submenu_id=non_existing_submenu_id
    )
    response = client.patch(
        url=route_url, 
        json=updating_submenu_data
    )

    assert response.status_code == 404
    assert response.json() == not_found_submenu_response


def test_delete_submenu(client, existing_menu_id, existing_submenu_id):
    route_url = ROUTE_PREFIXES["submenu"].format(
        menu_id=existing_menu_id,
        submenu_id=existing_submenu_id
    )
    response = client.delete(
        url=route_url
    )

    assert response.status_code == 200
    assert response.json() == deleted_submenu_response


def test_read_submenu_success(client, existing_menu_id, existing_submenu_id):
    route_url = ROUTE_PREFIXES["submenu"].format(
        menu_id=existing_menu_id,
        submenu_id=existing_submenu_id
    )
    response = client.get(
        url=route_url
    )

    assert response.status_code == 200
    assert response.json() == {
        **read_submenu_data,
        "id": existing_submenu_id,
    }


def test_read_submenu_fail(client, existing_menu_id, non_existing_submenu_id):
    route_url = ROUTE_PREFIXES["submenu"].format(
        menu_id=existing_menu_id,
        submenu_id=non_existing_submenu_id
    )
    response = client.get(
        url=route_url
    )

    assert response.status_code == 404
    assert response.json() == not_found_submenu_response


def test_read_all_submenus(client, existing_menu_id, existing_submenu_id):
    route_url = ROUTE_PREFIXES["submenus"].format(
        menu_id=existing_menu_id
    )
    response = client.get(
        url=route_url
    )

    assert response.status_code == 200

    response_json = response.json()
    assert response_json == [
        {
            **read_submenu_data,
            "id": existing_submenu_id,
        }
    ]