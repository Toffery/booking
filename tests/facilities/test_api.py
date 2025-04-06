async def test_get_facilities(ac):
    response = await ac.get("/facilities/")
    assert response.status_code == 200


async def test_add_facility(admin_ac):
    response = await admin_ac.post("/facilities/", json={"title": "test_facility"})
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "test_facility"


async def test_add_facility_not_admin(authenticated_ac):
    response = await authenticated_ac.post("/facilities/", json={"title": "test_facility"})
    assert response.status_code == 403
