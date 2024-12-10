async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels/",
        params={
            "date_from": "2024-10-18",
            "date_to": "2024-10-25",
        }
    )
    assert response.status_code == 200
