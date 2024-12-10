from datetime import date

import pytest


@pytest.mark.parametrize(
    "room_id, date_from, date_to, price, status_code",
    [
        (1, "2024-10-18", "2024-10-25", 24500, 200),
        (1, "2024-10-18", "2024-10-25", 24500, 200),
        (1, "2024-10-18", "2024-10-25", 24500, 500),
        (1, "2024-11-18", "2024-11-25", 24500, 200),
    ]
)
async def test_create_booking(
        room_id,
        date_from,
        date_to,
        price,
        status_code,
        authenticated_ac,
        db
):
    response = await authenticated_ac.post(
        "/bookings/",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        assert response.json()["data"]["room_id"] == room_id
        assert response.json()["data"]["date_from"] == date_from
        assert response.json()["data"]["date_to"] == date_to

        days = (date.fromisoformat(date_to) - date.fromisoformat(date_from)).days
        price_needed = price * days

        assert response.json()["data"]["price"] == price_needed


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


async def test_get_my_bookings(authenticated_ac):
    response = await authenticated_ac.get("/bookings/me")
    assert response.status_code == 200


@pytest.fixture(scope="session")
async def delete_bookings(ac, db):
    await db.bookings.delete_all_rows()


async def test_add_and_get_my_bookings(delete_bookings):
    pass
