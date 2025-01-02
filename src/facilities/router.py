from fastapi import APIRouter

from src.dependencies import DBDep
from src.exceptions import FacilityNotFoundException
from src.facilities.schemas import FacilityIn

from fastapi_cache.decorator import cache

from src.httpexceptions import FacilityNotFoundHTTPException
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Facilities"])

FACILITY_CACHE_EXP = 60


@router.get("/")
@cache(expire=10)
async def get_facilities(
    db: DBDep,
):
    return await FacilityService(db).get_facilities()


@router.get("/{facility_id}")
@cache(expire=FACILITY_CACHE_EXP)
async def get_facility_by_id(facility_id: int, db: DBDep):
    try:
        return await FacilityService(db).get_facility_by_id(facility_id)
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException


@router.post("/")
async def create_facility(db: DBDep, facility_data: FacilityIn):
    created_facility = await FacilityService(db).create_facility(facility_data)

    return {"message": "Facility created", "data": created_facility}


@router.post("/{facility_id}")
async def update_facility(db: DBDep, facility_id: int, facility_data: FacilityIn):
    try:
        updated_facility = await FacilityService(db).update_facility(facility_id, facility_data)
        return {"message": "Facility updated", "data": updated_facility}
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException


@router.delete("/{facility_id}")
async def delete_facility(db: DBDep, facility_id: int):
    try:
        await FacilityService(db).delete_facility(facility_id)
        return {"message": "Facility deleted"}
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException
