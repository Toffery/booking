async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels/",
        params={
            "date_from": "2024-10-18",
            "date_to": "2024-10-25",
        },
    )
    assert response.status_code == 200

    response = await ac.get(
        "/hotels/",
        params={
            "date_from": "2024-10-25",
            "date_to": "2024-10-18",
        },
    )
    assert response.status_code == 409


async def test_get_hotel_by_id(ac):
    response = await ac.get("/hotels/1")
    assert response.status_code == 200

    response = await ac.get("/hotels/100")
    assert response.status_code == 404


async def test_create_hotel_not_admin(authenticated_ac):
    response = await authenticated_ac.post(
        "/hotels/",
        json={
            "title": "test_hotel",
            "location": "test_location",
        },
    )
    assert response.status_code == 403, "Hotel created by not admin user"


async def test_create_hotel(admin_ac):
    response = await admin_ac.post(
        "/hotels/",
        json={
            "title": "test_hotel",
            "location": "test_location",
        },
    )
    assert response.status_code == 200
    assert response.json()["data"]["id"]
    assert response.json()["data"]["title"] == "test_hotel"
    assert response.json()["data"]["location"] == "test_location"


async def test_update_and_patch_hotel(admin_ac):
    response = await admin_ac.put(
        "/hotels/1",
        json={
            "title": "updated_test_hotel",
            "location": "updated_test_location",
        },
    )
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 1
    assert response.json()["data"]["title"] == "updated_test_hotel"
    assert response.json()["data"]["location"] == "updated_test_location"

    response = await admin_ac.put(
        "/hotels/100",
        json={
            "title": "updated_test_hotel",
            "location": "updated_test_location",
        },
    )
    assert response.status_code == 404

    response = await admin_ac.patch(
        "/hotels/1",
        json={
            "title": "patched_test_hotel",
        },
    )
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 1
    assert response.json()["data"]["title"] == "patched_test_hotel"
    assert response.json()["data"]["location"] == "updated_test_location"

    response = await admin_ac.patch(
        "/hotels/1",
        json={
            "location": "patched_test_location",
        },
    )
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 1
    assert response.json()["data"]["title"] == "patched_test_hotel"
    assert response.json()["data"]["location"] == "patched_test_location"
