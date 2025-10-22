from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

users_list = [
    User(id=1, name="Jose", surname="Iglesias", age=20),
    User(id=2, name="Pepito", surname="Perez", age=20),
    User(id=3, name="JoseMa", surname="Maya", age=20)
]


@app.get("/users")
def get_users():
    """Devuelve toda la lista de usuarios"""
    return users_list


@app.get("/users/{id_user}")
def get_user_by_id(id_user: int):
    """Devuelve un usuario por su ID desde la ruta"""
    return search_user(id_user)


@app.get("/users/")
def get_user(id: int):
    return search_user(id)

@app.post("/users", status_code=201, response_model= User)
def addUser(user: User):
    #Calculamos el siguiente id y se lo ponemos al que ha entrado de parámetro
    user.id = next_id()
    users_list.append(user)
    return user

@app.put("/users/{id}", response_model= User)
def modify_user(id: int, user:User):
    #Método enumerate devuelve el índice de la lista
    #y el usuario almacenado en dicho índice
    for index,saved_user in enumerate(users_list):
        if saved_user.id == id:
            user.id = id
            users_list[index] = user
            return user
    
    raise HTTPException(status_code = 404, detail= "User not found")

@app.delete("/users/{id}")
def delete_user(id:int):
    for saved_user in users_list:
        if saved_user.id == id:
            users_list.remove(saved_user)
            return {}
    raise HTTPException(status_code=404, detail="user not found")

def search_user(id: int):
    """Función auxiliar para buscar un usuario por su ID"""
    users = [user for user in users_list if user.id == id]
    if users:
        return users[0]
    raise HTTPException(status_code = 404, detail= "User not found")


def next_id():
    return max(users_list, key=lambda user: user.id).id + 1