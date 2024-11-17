from fastapi import APIRouter
from src.dependencies import PaginatorDep, DBDep

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

