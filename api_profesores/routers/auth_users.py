from fastapi import APIRouter, Depends, HTTPException
import fastapi
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
#Libreria JWT
import jwt
#Para trabajar las excepciones de los tokens
from jwt.exceptions import InvalidTokenError
#Libreria para aplicar el hash a la contraseña
from pwdlib import PasswordHash

router = fastapi.APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl = "login")

#Definimos el algoritmo de cifrado
ALGORITHM = "HS256"

#Duracion del token 
ACCESS_TOKEN_EXPIRE_MINUTES = 5

#Clave que se utilizará como semilla para generar el token 
#openssl rand -hex 32 en git bash 
SECRET_KEY = "75bd9345ec6f051a3abae248c0fdb871247e49df76edea657e319d58f6bdc75c"


#Objeto que se utilizará para el cálculo del hash y la verificación
#de contraseñas
password_hash = PasswordHash.recommended()
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "elenarg": {
        "username": "elenarg",
        "full_name": "Elena Rivero",
        "email": "elena.rivero@iesnervion.es",
        "disabled": False,
        "password": "123456"
    },
    "paquito": {
        "username": "paquito",
        "full_name": "Paco Pérez",
        "email": "paco.perez@iesnervion.es",
        "disabled": True,
        "password": "1234"
    },
    "IvanCarrascosa": {
    "username": "IvanCarrascosa",
    "full_name": "Yoops",
    "email": "ivan.carrascosa@iesnervion.es",
    "disabled": False,
    "password": "$argon2id$v=19$m=65536,t=3,p=4$m780unecJIrwbNWu5dRpSQ$mYsAsNNeDfxp8ypsVNubHqKiq86xP3H1ZhpiDuK91LQ"
    }
}

@router.post("/register", status_code = 201)
def register(user: UserDB):
    if user.username not in users_db:
        hashed_password = password_hash.hash(user.password)
        user.password = hashed_password
        users_db[user.username] = user
        return user
    else:
        raise HTTPException(status_code= 409, detail="User alredy exists") 

#async def login(form: OAuth2PasswordRequestForm = Depends()):