from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from routers.auth_users import auth_user
from db.models.alumno import Alumno
from db.schemas.alumno import alumno_schema, alumnos_schema
from db.client import db_client

from db.models.colegio import Colegio
from db.schemas.colegio import colegio_schema, colegios_schema

router = APIRouter(prefix = "/colegios", tags=["colegios"])

@router.get("/", response_model= list[Colegio])
async def colegios():
    # El método find() sin parámetros devuelve todos los registros
    # de la base de datos
    return colegios_schema(db_client.test.colegios.find())

# Método get por id
@router.get("/{id}", response_model=Colegio)
async def colegio(id: str):
    return search_colegio_id(id)

@router.get("{id_colegio}/alumnos", response_model=list[Alumno])
async def alumnos_id_colegio(id_colegio: str): 
    return search_alumno_idColegio(id_colegio)


@router.post("/", response_model=Colegio, status_code=201)
async def add_user(colegio: Colegio, authorized = Depends(auth_user)): 
    if type(search_colegio(colegio.nombre, colegio.distrito)) == Colegio:
        raise HTTPException(status_code=409, detail="Colegio already exists")
    
    colegio_dict = colegio.model_dump()
    del colegio_dict["id"]
    # Añadimos el usuario a nuestra base de datos
    # También podemos obtner con inserted_id el id que la base de datos
    # ha generado para nuestro usuario
    id= db_client.test.colegios.insert_one(colegio_dict).inserted_id

    # Añadimos el campo id a nuestro diccionario. Hay que hacerle un cast
    # a string puesto que el id en base de datos se almacena como un objeto,
    # no como un string
    colegio_dict["id"] = str(id)

    # La respuesta de nuestro método es el propio usuario añadido
    # Creamos un objeto de tipo User a partir del diccionario user_dict
    return Colegio(**colegio_dict)

@router.delete("/{id}", response_model=Colegio)
async def delete_colegio(id:str, authorized = Depends(auth_user)):
   found = db_client.test.colegios.find_one_and_delete({"_id":ObjectId(id)})
   if not found:
       raise HTTPException(status_code=404, detail="Profesor not found")
   
   return Colegio(**colegio_schema(found))

def search_colegio_id(id: str):    
    # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
    # así que la controlamos
    try:
        # El id en base de datos no se guarda como un string, sino que es un objeto 
        # Realizamos la conversión
        # CORREGIDO: cambiar 'users' por 'profesores'
        colegio = colegio_schema(db_client.test.colegios.find_one({"_id":ObjectId(id)}))
        # Necesitamos convertirlo a un objeto User. 
        return Colegio(**colegio)
    except:
        return {"error": "Colegio not found"}

def search_colegio(nombre: str, distrito: str):
    # La búsqueda me devuelve un objeto del tipo de la base de datos.
    # Necesitamos convertirlo a un objeto User. 
    try:
        # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
        # así que la controlamos
        colegio = colegio_schema(db_client.test.colegios.find_one({"nombre":nombre, "distrito":distrito}))
        return Colegio(**colegio)
    except:
        return {"error": "Colegio not found"}
    
def search_alumno_idColegio(id_colegio: str):    
    # El id en base de datos no se guarda como un string, sino que es un objeto 
    # Realizamos la conversión
    # CORREGIDO: cambiar 'users' por 'profesores'
    alumnos = alumnos_schema(db_client.test.alumnos.find({"id_colegio":id_colegio}))
    # Necesitamos convertirlo a un objeto User. 
    return [alumno_schema(alumno) for alumno in alumnos]