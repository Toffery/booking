from fastapi import APIRouter

from src.dependencies import DBDep
from src.facilities.schemas import FacilityIn

from fastapi_cache.decorator import cache


router = APIRouter(prefix="/facilities", tags=["Facilities"])

FACILITY_CACHE_EXP = 60


@cache(expire=10)
@router.get("/")
async def get_facilities(
        db: DBDep,
):
    return await db.facilities.get_all()


@cache(expire=FACILITY_CACHE_EXP)
@router.get("/{facility_id}")
async def get_single_facility(
        facility_id: int,
        db: DBDep
):
    return await db.facilities.get_one_or_none(id=facility_id)
    
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
