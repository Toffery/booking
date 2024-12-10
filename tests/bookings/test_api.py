# async def test_create_booking(authenticated_ac, db):
#     rooms = await db.rooms.get_all()
#     room_id = rooms[0].id
#     response = await authenticated_ac.post(
#         "/bookings/",
#         json={
#             "room_id": room_id,
#             "date_from": "2024-10-18",
#             "date_to": "2024-10-25",
#         }
#     )
#     assert response.status_code == 200

async def test_get_my_bookings(authenticated_ac):
    response = await authenticated_ac.get("/bookings/me")
    assert response.status_code == 200

async def test_create_not_authenticated_booking(ac):
    response = await ac.post(
        "/bookings/",
        json={
            "room_id": 1,
            "date_from": "2024-10-18",
            "date_to": "2024-10-25",
        }
    )
    assert response.status_code == 401
