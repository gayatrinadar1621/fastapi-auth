from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.auth.models import UserAuthModel
from fastapi.exceptions import HTTPException
from fastapi import status

class Service:
    async def is_user_exists(self, email:str, session:AsyncSession):
        statement = select(UserAuthModel).where(UserAuthModel.email == email)
        result = await session.execute(statement)
        user_present = result.scalar_one_or_none()
        return user_present
    
    async def create_user(self, user_data:UserAuthModel, session:AsyncSession):
        existing_user = await self.is_user_exists(user_data.email, session)
        print("existing_user", existing_user)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        
        # add user to database
        user_dict = user_data.model_dump()
        newuser = UserAuthModel(**user_dict)
        session.add(newuser)
        await session.commit()
        await session.refresh(newuser)
        return newuser
