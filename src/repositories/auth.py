from sqlalchemy import select
from src.users.models import User
from src.users.schemas import UserInDB, UserSchema
from src.repositories.baserepo import BaseRepository


class AuthRepository(BaseRepository):
    model = User
    schema = UserSchema

    async def get_user_in_db(self, email: str | None = None, username: str | None = None) -> UserInDB | None:
        query = select(self.model)
        if email:
            query = query.filter_by(email=email)
        elif username:
            query = query.filter_by(username=username)

        result = await self.session.execute(query)
        user = result.scalars().one()
        return UserInDB.model_validate(user)
