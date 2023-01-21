from app.endpoints import ROUTE_PREFIXES
from .resources.menu import (
    read_menu_data, creating_menu_data, updating_menu_data,
    deleted_menu_response, not_found_menu_response
)


def test_create_menu(client):
    route_url = ROUTE_PREFIXES["menu"] + "/"
    response = client.post(
        url=route_url, json=creating_menu_data
    )

    assert response.status_code == 201

    response_json = response.json()
    assert response_json == {
        "id": response_json["id"],
        **creating_menu_data
    }


def test_update_menu_success(client, existing_menu_id):
    route_url = "{}/{}".format(ROUTE_PREFIXES["menu"], existing_menu_id)
    response = client.patch(
        url=route_url, json=updating_menu_data
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": existing_menu_id,
        **updating_menu_data
    }


def test_update_menu_fail(client, non_existing_menu_id):
    route_url = "{}/{}".format(ROUTE_PREFIXES["menu"], non_existing_menu_id)
    response = client.patch(
        url=route_url, json=updating_menu_data
    )

    assert response.status_code == 404
    assert response.json() == not_found_menu_response


def test_delete_menu(client, existing_menu_id):
    route_url = "{}/{}".format(ROUTE_PREFIXES["menu"], existing_menu_id)
    response = client.delete(
        url=route_url
    )

    assert response.status_code == 200
    assert response.json() == deleted_menu_response


def test_read_menu_success(client, existing_menu_id):
    route_url = "{}/{}".format(ROUTE_PREFIXES["menu"], existing_menu_id)
    response = client.get(
        url=route_url
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": existing_menu_id,
        **read_menu_data
    }


def test_read_menu_fail(client, non_existing_menu_id):
    route_url = "{}/{}".format(ROUTE_PREFIXES["menu"], non_existing_menu_id)
    response = client.get(
        url=route_url
    )

    assert response.status_code == 404
    assert response.json() == not_found_menu_response


def test_read_all_menus(client, existing_menu_id):
    route_url = ROUTE_PREFIXES["menu"] + "/"
    response = client.get(
        url=route_url
    )

    assert response.status_code == 200

    response_json = response.json()
    assert response_json == [
        {
            "id": existing_menu_id,
            **read_menu_data
        }
    ]