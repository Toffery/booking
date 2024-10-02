from sqlalchemy import select
from src.auth.models import User
from src.auth.schemas import UserInDB, UserSchema
from repositories.baserepo import BaseRepository


class AuthRepository(BaseRepository):
    model = User
    schema = UserSchema

    async def get_user_in_db(self, email: str) -> UserInDB | None:
        query = (
            select(self.model)
            .filter_by(email=email)
        )
        result = await self.session.execute(query)
        user = result.scalars().one()
        return UserInDB.model_validate(user)
