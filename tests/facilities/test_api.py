async def test_get_facilities(ac):
    response = await ac.get("/facilities/")
    assert response.status_code == 200


async def test_add_facility(ac):
    response = await ac.post("/facilities/", json={"title": "test_facility"})
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "test_facility"
