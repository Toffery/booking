async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels/",
        params={
            "date_from": "2024-10-18",
            "date_to": "2024-10-25",
        }
    )
    assert response.status_code == 200


async def test_get_my_bookings(authenticated_ac):
    response = await authenticated_ac.get("/bookings/me")
    assert response.status_code == 200
