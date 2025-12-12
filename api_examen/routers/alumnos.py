from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from routers.auth_users import auth_user
from db.schemas.colegio import colegio_schema
from db.client import db_client
from db.models.alumno import Alumno
from db.schemas.alumno import alumno_schema, alumnos_schema

router = APIRouter(prefix = "/alumnos", tags=["alumnos"])

@router.get("/", response_model= list[Alumno])
async def alumnos():
    # El método find() sin parámetros devuelve todos los registros
    # de la base de datos
    return alumnos_schema(db_client.test.alumnos.find())

# Método get tipo query. Sólo busca por id
@router.get("", response_model=list[Alumno])
async def alumno(curso: str):
    return search_alumno_curso(curso)

@router.get("", response_model=list[Alumno])
async def alumno(distrito: str):
    return search_alumno_distrito(distrito)

@router.get("", response_model=list[Alumno])
async def alumno(distrito: str, curso: str):
    return search_alumno_distrito_curso(distrito, curso)

@router.post("", response_model=Alumno, status_code=201)
async def add_user(alumno: Alumno, authorized = Depends(auth_user)):
    #No compruebo si el alumno ya existe porque puede haber alumnos con mismo nombre y apellidos y con la misma info
    alumno_dict = alumno.model_dump()
    del alumno_dict["id"]
    if alumno_dict["curso"] in ["1ESO", "2ESO", "3ESO", "4ESO", "1BACH", "2BACH"]:
        try:
            if alumno_dict["id_colegio"] == colegio_schema(db_client.test.colegios.find_one({"_id":ObjectId(alumno_dict["id_colegio"])}))["id"]:
                id= db_client.test.alumnos.insert_one(alumno_dict).inserted_id
                alumno_dict["id"] = str(id)
                return Alumno(**alumno_dict)
            else:
                raise(HTTPException(status_code=404, detail="Id de colegio no existente"))
        except:
            raise(HTTPException(status_code=404, detail="Id de colegio no existente"))
    else:
        raise(HTTPException(status_code=404, detail="Curso no válido"))

@router.put("/{id}", response_model=Alumno)
async def modify_alumno(id: str, new_alumno: Alumno, authorized = Depends(auth_user)):
    # Convertimos el usuario a un diccionario
    alumno_dict = new_alumno.model_dump()
    # Eliminamos el id en caso de que venga porque no puede cambiar
    del alumno_dict["id"] 
    alumno = search_alumno_id(id)  
    if alumno:
        if alumno_dict["curso"] in ["1ESO", "2ESO", "3ESO", "4ESO", "1BACH", "2BACH"]:
            try:
                if alumno_dict["id_colegio"] == colegio_schema(db_client.test.colegios.find_one({"_id":ObjectId(alumno_dict["id_colegio"])}))["id"]:
                    db_client.test.alumnos.find_one_and_replace({"_id":ObjectId(id)}, alumno_dict)
                    # Buscamos el objeto en base de datos y lo retornamos, así comprobamos que efectivamente
                    # se ha modificado
                    return search_alumno_id(id)
                else:
                    raise(HTTPException(status_code=404, detail="Id de colegio no existente"))
            except:
                raise(HTTPException(status_code=404, detail="Id de colegio no existente"))
        else:
            raise(HTTPException(status_code=404, detail="Curso no válido"))    
    else:
        raise HTTPException(status_code=404, detail="Alumno not found")

def search_alumno_id(id: str):    
    # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
    # así que la controlamos
    try:
        # El id en base de datos no se guarda como un string, sino que es un objeto 
        # Realizamos la conversión
        # CORREGIDO: cambiar 'users' por 'profesores'
        alumno = alumno_schema(db_client.test.alumnos.find_one({"_id":ObjectId(id)}))
        # Necesitamos convertirlo a un objeto User. 
        return Alumno(**alumno)
    except:
        return {"error": "Alumno not found"}
    
def search_alumno_curso(curso: str):    
    # El id en base de datos no se guarda como un string, sino que es un objeto 
    # Realizamos la conversión
    # CORREGIDO: cambiar 'users' por 'profesores'
    alumnos = alumnos_schema(db_client.test.alumnos.find({"curso":curso}))
    # Necesitamos convertirlo a un objeto User. 
    return [alumno_schema(alumno) for alumno in alumnos]

def search_alumno_distrito(distrito: str):    
    # El id en base de datos no se guarda como un string, sino que es un objeto 
    # Realizamos la conversión
    # CORREGIDO: cambiar 'users' por 'profesores'
    alumnos = alumnos_schema(db_client.test.alumnos.find({"distrito":distrito}))
    # Necesitamos convertirlo a un objeto User. 
    return [alumno_schema(alumno) for alumno in alumnos]

def search_alumno_distrito_curso(distrito: str, curso: str):    
    # El id en base de datos no se guarda como un string, sino que es un objeto 
    # Realizamos la conversión
    # CORREGIDO: cambiar 'users' por 'profesores'
    alumnos = alumnos_schema(db_client.test.alumnos.find({"distrito":distrito, {"curso"}: curso}))
    # Necesitamos convertirlo a un objeto User. 
    return [alumno_schema(alumno) for alumno in alumnos]