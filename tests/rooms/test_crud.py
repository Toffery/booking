from src.rooms.schemas import RoomCreate, RoomInDB, RoomUpdate, RoomPatch


async def test_rooms_without_facilities_crud(db):
    hotel_id: int = 1
    room_to_create: RoomCreate = RoomCreate(
        hotel_id=hotel_id,
        title="Test room",
        description="Test description",
        price=100,
        quantity=3
    )
    created_room: RoomInDB = await db.rooms.add(room_to_create)
    assert created_room
    assert created_room.hotel_id == hotel_id
    assert created_room.title == "Test room"
    assert created_room.description == "Test description"
    assert created_room.price == 100
    assert created_room.quantity == 3

    room_data_to_update = RoomUpdate(
        title="Updated room",
        description="Updated description",
        price=200,
        quantity=4
    )
    updated_room: RoomInDB = await db.rooms.edit(
        room_data_to_update,
        id=created_room.id,
        hotel_id=hotel_id
    )
    assert updated_room
    assert updated_room.hotel_id == hotel_id
    assert updated_room.title == "Updated room"
    assert updated_room.description == "Updated description"
    assert updated_room.price == 200
    assert updated_room.quantity == 4

    room_data_to_patch = RoomPatch(
        title="Patched room",
        price=300,
    )
    patched_room: RoomInDB = await db.rooms.edit(
        room_data_to_patch,
        exclude_unset=True,
        id=created_room.id,
        hotel_id=hotel_id
    )
    assert patched_room
    assert patched_room.hotel_id == hotel_id
    assert patched_room.title == "Patched room"
    assert patched_room.description == "Updated description"
    assert patched_room.price == 300
    assert patched_room.quantity == 4

    await db.rooms.delete(id=created_room.id, hotel_id=hotel_id)
    deleted_room = await db.rooms.get_one_or_none(id=created_room.id, hotel_id=hotel_id)
    assert not deleted_room

    await db.commit()
