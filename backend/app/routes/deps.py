from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.models import User
from app.security import SECRET_KEY, ALGORITHM
import jwt
from app.database import SessionLocal
from app.dependencies import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def is_admin(current_user: User = Depends(get_current_user)):
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
