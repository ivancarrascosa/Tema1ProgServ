from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Entidad usuario
class Profesor(BaseModel):
    id: int
    DNI: str
    nombre: str
    apellidos: str
    telefono: int
    direccion: str
    cuentaBancaria: str

profesores_list = [
    Profesor(id=1, DNI="12345678A", nombre="Roberto", apellidos="Morano", telefono=600123456, direccion="Calle Mayor 1, Madrid", cuentaBancaria="ES1234567890123456789012"),
    Profesor(id=2, DNI="23456789B", nombre="Francisco", apellidos="Manuel", telefono=600234567, direccion="Calle Luna 12, Sevilla", cuentaBancaria="ES2345678901234567890123"),
    Profesor(id=3, DNI="34567890C", nombre="Jose", apellidos="Iglesias", telefono=600345678, direccion="Av. del Sol 3, Valencia", cuentaBancaria="ES3456789012345678901234"),
    Profesor(id=4, DNI="45678901D", nombre="Lucía", apellidos="Ramirez", telefono=600456789, direccion="Plaza del Pilar 4, Zaragoza", cuentaBancaria="ES4567890123456789012345"),
    Profesor(id=5, DNI="56789012E", nombre="Marta", apellidos="Lopez", telefono=600567890, direccion="Calle Verde 5, Bilbao", cuentaBancaria="ES5678901234567890123456"),
    Profesor(id=6, DNI="67890123F", nombre="Antonio", apellidos="Nuniez", telefono=600678901, direccion="Av. Libertad 6, Málaga", cuentaBancaria="ES6789012345678901234567"),
    Profesor(id=7, DNI="78901234G", nombre="Sara", apellidos="Lopez", telefono=600789012, direccion="Calle Azul 7, Alicante", cuentaBancaria="ES7890123456789012345678"),
    Profesor(id=8, DNI="89012345H", nombre="Pedro", apellidos="Gomez", telefono=600890123, direccion="Paseo del Río 8, Valladolid", cuentaBancaria="ES8901234567890123456789"),
    Profesor(id=9, DNI="90123456I", nombre="Laura", apellidos="Martinez", telefono=600901234, direccion="Camino Real 9, Granada", cuentaBancaria="ES9012345678901234567890"),
    Profesor(id=10, DNI="01234567J", nombre="Carlos", apellidos="Sanchez", telefono=600012345, direccion="Ronda Sur 10, Coruña", cuentaBancaria="ES0123456789012345678901"),
    ]

def buscar_profesor_ID(id_profesor: int):
    users = [i for i in profesores_list if i.id == id_profesor]

    if len(users) != 0:
        return users[0]
    else:
        raise HTTPException(status_code=404, detail="Profesor not found")

@app.get("/profesores")
def profesores():
    return profesores_list

@app.get("/profesores/{id_profesor}")
def get_profesor_ID(id_profesor: int):
    return buscar_profesor_ID(id_profesor)

@app.get("/profesores/")
def get_profesor_query(id: int):
    return buscar_profesor_ID(id)

@app.post("/profesores", status_code=201, response_model= Profesor)
def post_profesor(profesor: Profesor):
    profesor.id = next_id()
    profesores_list.append(profesor)
    return profesor

@app.put("/profesores/{id}", response_model = Profesor)
def modify_profesor(id: int, profesor: Profesor):
    for index, saved_profesor in enumerate(profesores_list):
        if saved_profesor.id == id:
            profesor.id = id 
            profesores_list[index] = profesor
            return profesor
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/profesores/{id}")
def delete_profesor(id: int):
    for profesor in profesores_list:
        if profesor.id == id:
            profesores_list.remove(profesor)
            return {}
    raise HTTPException(status_code=404, detail="user not found")

def next_id():
    return max(profesores_list, key = lambda profesor: profesor.id).id + 1