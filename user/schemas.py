from pydantic import BaseModel
from typing import Optional

class SignUpInput(BaseModel):
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = None
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            'example': {
                "username": "myname",
                "email": "myemail@gmail.com",
                "password": "mypassword",
                "is_staff": False,
                "is_active": True
            }
        }

# Modelo de saída (quando retorna um usuário já criado)
class SignUpOutput(SignUpInput):
    id: int

    class Config:
        from_attributes = True


class LoginModel(BaseModel):
    username:str
    password:str
    