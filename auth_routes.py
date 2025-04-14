from fastapi import APIRouter, status, Request, Header
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from postgres.database import Session, engine
from postgres.schemas import SignUpInput, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from jwt_handler import create_access_token, create_refresh_token, decode_token


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
    

#login route
@auth_router.post('/login', status_code=200)
async def login(user:LoginModel):
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        payload = {"subject": db_user.username}
        access_token = create_access_token(payload)
        refresh_token = create_refresh_token(payload)
        print("Access token:", access_token)
        print("Payload do token:", decode_token(access_token))

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
async def get_me(authorization: str = Header(..., alias="Authorization")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")

    parts = authorization.split(" ")
    if len(parts) != 2:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    token = parts[1]

    try:
        payload = decode_token(token)
        print("Payload recebido:", payload)
        username = payload.get("subject")

        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido: campo 'subject' ausente.")
        
        # Verifica se o usuário existe no banco
        db_user = session.query(User).filter(User.username == username).first()

        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

        if not db_user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo.")

        # Tudo certo
        return {
            "username": db_user.username,
            "email": db_user.email,
            "is_active": db_user.is_active,
            "is_staff": db_user.is_staff
        }

    except Exception as e:
        print("Erro ao decodificar:", str(e))
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))