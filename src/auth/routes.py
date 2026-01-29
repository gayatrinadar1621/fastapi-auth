from fastapi import APIRouter, status, Depends
from src.auth.models import CreateUserModel, UserAuthModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.services import Service
user_router = APIRouter()
auth_service = Service()

@user_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserAuthModel)
async def user_signup(user_data:CreateUserModel, session:AsyncSession = Depends(get_session)):
    result = await auth_service.create_user(user_data, session)
    print("result", result)
    return result


