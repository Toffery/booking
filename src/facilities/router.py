import json
from fastapi import APIRouter
from src.dependencies import PaginatorDep, DBDep
from src.facilities.schemas import FacilityIn
from src.core.setup import redis_manager

router = APIRouter(prefix="/facilities", tags=["Facilities"])

FACILITY_CACHE_EXP = 60

@router.get("/")
async def get_facilities(
        paginator: PaginatorDep,
        db: DBDep,
):
    offset = (paginator.page - 1) * paginator.per_page
    limit = paginator.per_page

    cached_facilities = await redis_manager.get(f"facilities:{offset}:{limit}")
    if cached_facilities:
        return json.loads(cached_facilities)
    else:
        facilities_objs = await db.facilities.get_all(
            limit=limit,
            offset=offset
        )
        dumped_facilities = json.dumps([f.model_dump() for f in facilities_objs])
        await redis_manager.set(
            key=f"facilities:{offset}:{limit}",
            value=dumped_facilities,
            exp=FACILITY_CACHE_EXP,
        )
        return facilities_objs


@router.get("/{facility_id}")
async def get_single_facility(
        facility_id: int,
        db: DBDep
):
    cached_facility = await redis_manager.get(f"facility_{facility_id}")
    if cached_facility:
        cached_facility = json.loads(cached_facility)
        return cached_facility
    else:
        facility_obj = await db.facilities.get_one_or_none(id=facility_id)
        dumped_facility = json.dumps(facility_obj.model_dump())
        await redis_manager.set(
            key=f"facility_{facility_id}", 
            value=dumped_facility,
            exp=FACILITY_CACHE_EXP,
        )
        return facility_obj

@router.post("/")
async def create_facility(
        db: DBDep,
        facility_data: FacilityIn
):
    ret_data = await db.facilities.add(facility_data)
    await db.commit()

    return {
        "message": "Facility created",
        "data": ret_data
    }

@router.post("/{facility_id}")
async def update_facility(
        db: DBDep,
        facility_id: int,
        facility_data: FacilityIn
):
    ret_data = await db.facilities.edit(
        id=facility_id,
        data=facility_data
    )
    await db.commit()

    return {
        "message": "Facility updated",
        "data": ret_data
    }

@router.delete("/{facility_id}")
async def delete_facility(
        db: DBDep,
        facility_id: int
):
    await db.facilities.delete(id=facility_id)
    await db.commit()

    return {
        "message": "Facility deleted"
    }
