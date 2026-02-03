from fastapi import APIRouter, status, Depends
from src.auth.models import CreateUserModel, UserAuthModel, LoginUserModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.services import Service
from src.auth.dependencies import get_current_user
from src.db.redis import get_refresh_token_data
user_router = APIRouter()
auth_service = Service()

@user_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserAuthModel)
async def user_signup(user_data:CreateUserModel, session:AsyncSession = Depends(get_session)):
    result = await auth_service.create_user(user_data, session)
    print("result", result)
    return result

@user_router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(user_data:LoginUserModel, session:AsyncSession = Depends(get_session)):
    result = await auth_service.user_login(user_data, session)
    print("result", result)
    return result

# dummy route to test protected route
@user_router.get("/dummy")
async def protected_dummy_route(user_details=Depends(get_current_user)):
    print("user_details",user_details)
    return {"message":"You are able to see this because you have been successfully authenticated.", "user_details":user_details}

# endpoint for refresh token
@user_router.post("/refresh")
async def refresh_token(refresh_token:str):
    token_data = get_refresh_token_data(refresh_token)
    print("token_data", token_data)


