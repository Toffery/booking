from src.auth.models import User
from src.auth.schemas import UserInDB
from repositories.baserepo import BaseRepository


class AuthRepository(BaseRepository):
    model = User
    schema = UserInDB
