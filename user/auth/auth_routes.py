from fastapi import APIRouter, status, Request, Header, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from user.schemas import SignUpInput, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from user.auth.jwt_handler import create_access_token, create_refresh_token, decode_token
from user.dependencies import get_current_user, get_db


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)



@auth_router.get('/')
async def hello():
    return {"message":"Hello! These route you both sign up and sign in an user."}


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user:SignUpInput, db: Session = Depends(get_db)):
    db_email = db.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User email already exists")
    
    db_username = db.query(User).filter(User.username == user.email).first()

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

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    

#login route
@auth_router.post('/login', status_code=200)
async def login(user:LoginModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        payload = {"subject": db_user.username}
        access_token = create_access_token(payload)
        refresh_token = create_refresh_token(payload)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")

@auth_router.post("/refresh")
async def refresh(request: Request):
    body = await request.json()
    refresh_token = body.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Refresh token missing")

    try:
        payload = decode_token(refresh_token)
        username = payload.get("subject")
        new_access_token = create_access_token({"subject": username})
        return {"access_token": new_access_token}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@auth_router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "email": current_user.email}