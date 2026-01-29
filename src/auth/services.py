from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.auth.models import CreateUserModel, UserAuthModel
from fastapi.exceptions import HTTPException
from fastapi import status
from src.auth.utils import hash_password

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
        print("passwordddddd", user_data.password)
        newuser = UserAuthModel(**user_dict)
        newuser.password = hash_password(user_dict["password"])
        session.add(newuser)
        await session.commit()
        await session.refresh(newuser)
        return newuser
