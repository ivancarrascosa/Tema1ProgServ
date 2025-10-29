from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

router = APIRouter(prefix= "/asignaturas", tags=["asignaturas"])

class Asignatura(BaseModel):
    id: int
    titulo: str
    num_horas: int
    id_profesor: int

asignaturas_list = [
    Asignatura(id=1,  titulo="Introducción a la Programación con Python", num_horas=30, id_profesor=1),
    Asignatura(id=2,  titulo="Bases de Datos con MySQL", num_horas=40, id_profesor=2),
    Asignatura(id=3,  titulo="Desarrollo Web con HTML, CSS y JavaScript", num_horas=45, id_profesor=3),
    Asignatura(id=4,  titulo="Programación Orientada a Objetos con Java", num_horas=50, id_profesor=4),
    Asignatura(id=5,  titulo="Sistemas Operativos y Administración Linux", num_horas=35, id_profesor=5),
    Asignatura(id=6,  titulo="Redes y Seguridad Informática", num_horas=30, id_profesor=6),
    Asignatura(id=7,  titulo="Análisis de Datos con Python y Pandas", num_horas=40, id_profesor=1),
    Asignatura(id=8,  titulo="Desarrollo de APIs con FastAPI", num_horas=35, id_profesor=3),
    Asignatura(id=9,  titulo="Inteligencia Artificial y Machine Learning", num_horas=60, id_profesor=7),
    Asignatura(id=10, titulo="Diseño de Interfaces con Figma", num_horas=25, id_profesor=8),
    Asignatura(id=11, titulo="Desarrollo Móvil con Flutter", num_horas=45, id_profesor=9),
    Asignatura(id=12, titulo="Gestión de Proyectos con Scrum y Agile", num_horas=20, id_profesor=10),
    Asignatura(id=13, titulo="Ciberseguridad y Criptografía", num_horas=50, id_profesor=6),
    Asignatura(id=14, titulo="Big Data con Hadoop y Spark", num_horas=55, id_profesor=7),
    Asignatura(id=15, titulo="DevOps con Docker y Kubernetes", num_horas=45, id_profesor=5)
]

def buscar_asignatura_id(id_asignatura: int):
    asignaturas = [i for i in asignaturas_list if i.id == id_asignatura]
    if len(asignaturas) != 0:
        return  asignaturas[0]
    else:
        raise HTTPException(status_code=404, detail="Asignatura no encontrada")

def next_id():
    return max(asignaturas_list, key = lambda asignatura: asignatura.id).id + 1
@router.get("/")
def get_asignaturas():
    return asignaturas_list

@router.get("/{id_asignatura}")
def get_asignatura_id(id_asignatura: int):
    return buscar_asignatura_id(id_asignatura)

@router.get("/")
def get_asignatura_query(id: int):
    return buscar_asignatura_id(id)

@router.post("/",status_code=201, response_model=Asignatura)
def post_asignatura(asignatura: Asignatura):
    asignatura.id = next_id()
    asignaturas_list.append(asignatura)
    return asignatura

@router.put("/{id_asignatura}", response_model=Asignatura)
def modify_asignatura(id_asignatura: int, asignatura: Asignatura):
    for index, saved_asignatura in enumerate(asignaturas_list):
        if saved_asignatura.id == id_asignatura:
            asignatura.id = saved_asignatura.id
            asignaturas_list[index] = asignatura
            return asignatura
    raise HTTPException(status_code=404, detail="Asignatura not found")

@router.delete("/{id}")
def delete_asignatura(id: int):
    for asignatura in asignaturas_list:
        if asignatura.id == id:
            asignaturas_list.remove(asignatura)
            return {}
    raise HTTPException(status_code=404, detail="Asignatura not found")