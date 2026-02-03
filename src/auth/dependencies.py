from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from src.auth.utils import verify_jwt_token

access_token_scheme = HTTPBearer()

def get_current_user(credentials=Depends(access_token_scheme)):
    print("Credentials received -->",credentials)
    token = credentials.credentials
    payload = verify_jwt_token(token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or Expired Token")
    
    return payload
