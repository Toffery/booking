import json
from fastapi import APIRouter

from src.core.redis_cache_decorator import redis_cache
from src.dependencies import PaginatorDep, DBDep
from src.facilities.schemas import FacilityIn
# from src.core.setup import redis_manager
from src.core.redis_cache_decorator import redis_cache

router = APIRouter(prefix="/facilities", tags=["Facilities"])

FACILITY_CACHE_EXP = 60

@router.get("/")
@redis_cache(exp=10)
async def get_facilities(
        paginator: PaginatorDep,
        db: DBDep,
):
    offset = (paginator.page - 1) * paginator.per_page
    limit = paginator.per_page

    return await db.facilities.get_all(
        limit=limit,
        offset=offset
    )

@router.get("/{facility_id}")
@redis_cache(exp=FACILITY_CACHE_EXP)
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
