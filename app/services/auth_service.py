from sqlalchemy.orm import Session
from app.services.user_service import get_user_by_email
from app.core.security import verify_password, create_access_token


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        return None, None
    if not verify_password(password, user.hashed_password):
        return None, None

    token = create_access_token({
        "user_id": user.id,
        "role": user.role
    })

    return token, user