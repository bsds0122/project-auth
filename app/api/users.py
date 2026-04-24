from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.user_service import get_all_users
from app.core.security import decode_token, JWTError
from app.schemas.user import UserOut

router = APIRouter()

auth_scheme = HTTPBearer()


# dependency to get current user
def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    try:
        payload = decode_token(token.credentials)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.get("/", response_model=List[UserOut])
def read_users(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")

    return get_all_users(db)