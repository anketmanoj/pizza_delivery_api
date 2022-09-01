from typing import Optional
from pydantic import BaseModel

from config import JWT_SECRET

class SignUpModel(BaseModel):
    id : Optional[int]
    username : str
    email : str
    password : str
    is_staff : Optional[bool]
    is_active : Optional[bool]

    class Config:
        orm_mode = True
        schema_extra={
            'example' : {
                "username" : "john",
                "email" : "john@doe.com",
                "password" : "hidden_password",
                "is_staff" : False,
                "is_active" : True
            }
        }

class Setting(BaseModel):
    authjwt_secret_key: str = JWT_SECRET

class LoginUser(BaseModel):
    username: str
    password: str