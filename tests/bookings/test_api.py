import asyncio
from datetime import date

import pytest


@pytest.fixture(scope="session")
async def delete_all_bookings(ac):
    response = await ac.delete("/bookings/delete_all")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "room_id, date_from, date_to, price, status_code",
    [
        (1, "2024-10-18", "2024-10-25", 24500, 200),
        (1, "2024-10-18", "2024-10-25", 24500, 200),
        (1, "2024-10-18", "2024-10-25", 24500, 500),
        (1, "2024-11-18", "2024-11-25", 24500, 200),
    ]
)
@pytest.mark.usefixtures("delete_all_bookings")
async def test_create_booking(
        room_id,
        date_from,
        date_to,
        price,
        status_code,
        authenticated_ac,
        db,
        delete_all_bookings,
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


@pytest.mark.parametrize(
    "room_id, date_from, date_to, price, status_code, num_of_bookings",
    [
        (1, "2024-10-18", "2024-10-25", 24500, 200, 1),
        (1, "2024-10-18", "2024-10-25", 24500, 200, 2)
    ]
)
async def test_add_and_get_my_bookings(
        room_id,
        date_from,
        date_to,
        price,
        status_code,
        num_of_bookings,
        authenticated_ac
):
    response = await authenticated_ac.post(
        "/bookings/",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code, response.json()

    my_bookings = await authenticated_ac.get("/bookings/me")
    assert my_bookings.status_code == 200
    assert len(my_bookings.json()) == num_of_bookings
