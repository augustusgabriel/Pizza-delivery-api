from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError
from postgres.database import Session, engine
from postgres.schemas import SignUpInput, SignUpOutput
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

session=Session(bind=engine)


@auth_router.get('/')
async def hello():
    return {"message":"Hellow World!"}


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user:SignUpInput):
    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User email already exists")
    
    db_username = session.query(User).filter(User.username == user.email).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Username already in use")
    
    new_user = User(
        username = user.username,
        email = user.email,
        password = generate_password_hash(user.password),
        is_active = user.is_active,
        is_staff = user.is_staff
    )

    session.add(new_user)

    try:
        session.commit()
        session.refresh(new_user)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )