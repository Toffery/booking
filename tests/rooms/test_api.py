async def test_get_rooms(ac):
    response = await ac.get(
        "/hotels/1/rooms",
        params={
            "date_from": "2024-10-18",
            "date_to": "2024-10-25",
        },
    )
    assert response.status_code == 200
    response = await ac.get(
        "/hotels/1/rooms",
        params={
            "date_from": "2024-10-18",
            "date_to": "2024-10-15",
        },
    )
    assert response.status_code == 409


async def test_get_room_by_id(ac):
    response = await ac.get("/hotels/1/rooms/1")
    assert response.status_code == 200

    response = await ac.get("/hotels/1/rooms/100")
    assert response.status_code == 404

    response = await ac.get("/hotels/100/rooms/1")
    assert response.status_code == 404


async def test_create_room(ac):
    response = await ac.post(
        "/hotels/1/rooms",
        json={
            "title": "test_room",
            "price": 1000,
            "quantity": 10,

        }
    )
    assert response.status_code == 200
    assert response.json()["data"]["id"]
    assert response.json()["data"]["title"] == "test_room"
    assert response.json()["data"]["price"] == 1000
    assert response.json()["data"]["quantity"] == 10


async def test_update_and_patch_room(ac):
    response = await ac.put(
        "/hotels/1/rooms/2",
        json={
            "title": "updated_test_room",
            "price": 2000,
            "quantity": 20,
            "description": "updated_test_description"
        }
    )
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 2
    assert response.json()["data"]["title"] == "updated_test_room"
    assert response.json()["data"]["price"] == 2000
    assert response.json()["data"]["quantity"] == 20

    response = await ac.put(
        "/hotels/1/rooms/100",
        json={
            "title": "updated_test_room",
            "price": 2000,
            "quantity": 20,
            "description": "updated_test_description"
        }
    )
    assert response.status_code == 404

    response = await ac.patch(
        "/hotels/1/rooms/2",
        json={
            "title": "patched_test_room",
        }
    )
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 2
    assert response.json()["data"]["title"] == "patched_test_room"
    assert response.json()["data"]["description"] == "updated_test_description"

    response = await ac.patch(
        "/hotels/1/rooms/2",
        json={
            "description": "patched_test_description"
        }
    )
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 2
    assert response.json()["data"]["title"] == "patched_test_room"
    assert response.json()["data"]["description"] == "patched_test_description"


    response = await ac.patch(
        "/hotels/1/rooms/100",
        json={
            "title": "patched_test_room",
            "description": "patched_test_description"
        }
    )
    assert response.status_code == 404


async def test_delete_room(ac):
    response = await ac.delete("/hotels/1/rooms/2")
    assert response.status_code == 200

    response = await ac.get("/hotels/1/rooms/2")
    assert response.status_code == 404
