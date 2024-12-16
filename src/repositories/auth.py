from sqlalchemy import select

from src.repositories.mappers.mappers import UserDataMapper
from src.users.models import User
from src.repositories.baserepo import BaseRepository
from src.users.schemas import UserInDB


class AuthRepository(BaseRepository):
    model = User
    mapper = UserDataMapper

    async def get_user_in_db(
        self, email: str | None = None, username: str | None = None
    ) -> UserInDB:
        query = select(self.model)
        if email:
            query = query.filter_by(email=email)
        elif username:
            query = query.filter_by(username=username)

        result = await self.session.execute(query)
        user = result.scalars().one()
        return self.mapper.map_to_domain_entity(user)

    # async def add(self, data: UserCreate):
    #     stmt = (
    #         insert(self.model).values(**data.model_dump(exclude_unset=True)).returning(self.model)
    #     )
    #     result = await self.session.execute(stmt)
    #     model = result.scalars().one()
    #     return self.mapper.map_to_domain_entity(model)
