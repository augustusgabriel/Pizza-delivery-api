from pydantic import BaseModel
from typing import Optional

class SignUpInput(BaseModel):
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        schema_extra = {
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
        orm_mode = True