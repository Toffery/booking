from fastapi import APIRouter
from src.dependencies import PaginatorDep, DBDep
from src.facilities.schemas import FacilityIn

router = APIRouter(prefix="/facilities", tags=["Facilities"])

@router.get("/")
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
