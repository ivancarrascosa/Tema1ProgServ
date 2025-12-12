from typing import Optional
from pydantic import BaseModel

class Usuario(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

class UserDB(Usuario):
    password: str