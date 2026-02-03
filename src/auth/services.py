from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.auth.models import CreateUserModel, UserAuthModel, LoginUserModel
from fastapi.exceptions import HTTPException
from fastapi import status
from src.auth.utils import hash_password, verify_password, create_jwt_token
from src.db.redis import store_refresh_token
import uuid
from datetime import timedelta

class Service:
    async def is_user_exists(self, email:str, session:AsyncSession):
        statement = select(UserAuthModel).where(UserAuthModel.email == email)
        result = await session.execute(statement)
        user_present = result.scalar_one_or_none()
        return user_present
    
    async def create_user(self, user_data:CreateUserModel, session:AsyncSession):
        existing_user = await self.is_user_exists(user_data.email, session)
        print("existing_user", existing_user)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        
        # add user to database
        user_dict = user_data.model_dump()
        newuser = UserAuthModel(**user_dict)
        newuser.password = hash_password(user_dict["password"])
        session.add(newuser)
        await session.commit()
        await session.refresh(newuser)
        return newuser
    
    async def user_login(self, user_data:LoginUserModel, session:AsyncSession):
        existing_user = await self.is_user_exists(user_data.email, session)
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        print("existing_user", existing_user)
        print("existing_user type", type(existing_user))
        is_valid_user = verify_password(user_data.password, existing_user.password)
        print("is_valid_user",is_valid_user)
        if not is_valid_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials")
        
        # user is valid, so create access token
        access_token = create_jwt_token(user_data={"user_id":existing_user.id , "email":existing_user.email})
        print("Created token -->", access_token)

        # user is valid, so create refresh token and store in redis database
        refresh_token = str(uuid.uuid4())
        await store_refresh_token(
            refresh_token,
            existing_user.id,
            existing_user.email,
            timedelta(days=7)
        )
        
        return {
            "message":"Login successful",
            "access_token" : access_token,
            "user_details" : {"user_id":existing_user.id, "email":existing_user.email}
        }
        

