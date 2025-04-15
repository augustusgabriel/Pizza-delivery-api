from fastapi import Header, HTTPException, Depends, status
from models import User
from postgres.database import Session, engine
from user.auth.jwt_handler import decode_token
from sqlalchemy.orm import Session as OrmSession


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    authorization: str = Header(..., alias="Authorization"),
    db: OrmSession = Depends(get_db)  # Usa a mesma session injetada
) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )

    parts = authorization.split(" ")
    if len(parts) != 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )

    token = parts[1]

    try:
        payload = decode_token(token)
        username = payload.get("subject")

        user = db.query(User).filter(User.username == username).first()

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not active or not found"
            )

        return user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Erro ao decodificar token: {str(e)}"
        )