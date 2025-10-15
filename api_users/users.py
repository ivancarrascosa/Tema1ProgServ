from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Entidad usuario
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

users_list = [
    User(id = 1, name= "Roberto", surname="Morano", age= 12),           
    User(id = 2, name= "Francisco", surname="Manue", age= 12),
    User(id = 3, name= "jose", surname= "iglesias", age=18)
    ]

@app.get("/users")
def users():
    return users_list

@app.get("/users/{id_user}")
def get_user(id_user: int):
    users = [i for i in users_list if i.id == id_user]

    return users[0] if len(users) != 0 else {"error" : "user not found"}