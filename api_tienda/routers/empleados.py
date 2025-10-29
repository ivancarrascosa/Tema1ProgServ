from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/empleados", tags=["empleados"])
class Empleado(BaseModel):
    id: int
    nombre: str
    apellidos: str
    telefono: int
    correo: str
    num_cuenta: str
    id_tienda: int

empleados_list = [
    Empleado(id=1, nombre="Laura", apellidos="García López", telefono=3511111111, correo="laura.garcia@empresa.com", num_cuenta="ES1200100000001111111111", id_tienda=1),
    Empleado(id=2, nombre="Carlos", apellidos="Pérez Díaz", telefono=3512222222, correo="carlos.perez@empresa.com", num_cuenta="ES1200100000002222222222", id_tienda=1),
    Empleado(id=3, nombre="Ana", apellidos="Martínez Ruiz", telefono=3513333333, correo="ana.martinez@empresa.com", num_cuenta="ES1200100000003333333333", id_tienda=2),
    Empleado(id=4, nombre="Javier", apellidos="Fernández Gómez", telefono=3514444444, correo="javier.fernandez@empresa.com", num_cuenta="ES1200100000004444444444", id_tienda=2),
    Empleado(id=5, nombre="Lucía", apellidos="Santos Herrera", telefono=3515555555, correo="lucia.santos@empresa.com", num_cuenta="ES1200100000005555555555", id_tienda=3),
    Empleado(id=6, nombre="Sergio", apellidos="Romero Castro", telefono=3516666666, correo="sergio.romero@empresa.com", num_cuenta="ES1200100000006666666666", id_tienda=3),
    Empleado(id=7, nombre="María", apellidos="Núñez Torres", telefono=3517777777, correo="maria.nunez@empresa.com", num_cuenta="ES1200100000007777777777", id_tienda=4),
    Empleado(id=8, nombre="Pablo", apellidos="Gutiérrez León", telefono=3518888888, correo="pablo.gutierrez@empresa.com", num_cuenta="ES1200100000008888888888", id_tienda=4),
    Empleado(id=9, nombre="Isabel", apellidos="López Serrano", telefono=3519999999, correo="isabel.lopez@empresa.com", num_cuenta="ES1200100000009999999999", id_tienda=5),
    Empleado(id=10, nombre="David", apellidos="Molina Rojas", telefono=3511010101, correo="david.molina@empresa.com", num_cuenta="ES1200100000010101010101", id_tienda=5),
    Empleado(id=11, nombre="Sofía", apellidos="Vega Campos", telefono=3511212121, correo="sofia.vega@empresa.com", num_cuenta="ES1200100000012121212121", id_tienda=6),
    Empleado(id=12, nombre="Miguel", apellidos="Delgado Cruz", telefono=3511313131, correo="miguel.delgado@empresa.com", num_cuenta="ES1200100000013131313131", id_tienda=6),
    Empleado(id=13, nombre="Paula", apellidos="Jiménez Morales", telefono=3511414141, correo="paula.jimenez@empresa.com", num_cuenta="ES1200100000014141414141", id_tienda=7),
    Empleado(id=14, nombre="Andrés", apellidos="Suárez Ramos", telefono=3511515151, correo="andres.suarez@empresa.com", num_cuenta="ES1200100000015151515151", id_tienda=7),
    Empleado(id=15, nombre="Clara", apellidos="Gómez Pardo", telefono=3511616161, correo="clara.gomez@empresa.com", num_cuenta="ES1200100000016161616161", id_tienda=8),
    Empleado(id=16, nombre="Adrián", apellidos="Ortega Navarro", telefono=3511717171, correo="adrian.ortega@empresa.com", num_cuenta="ES1200100000017171717171", id_tienda=8),
    Empleado(id=17, nombre="Elena", apellidos="Reyes Bravo", telefono=3511818181, correo="elena.reyes@empresa.com", num_cuenta="ES1200100000018181818181", id_tienda=9),
    Empleado(id=18, nombre="Rubén", apellidos="Campos Díaz", telefono=3511919191, correo="ruben.campos@empresa.com", num_cuenta="ES1200100000019191919191", id_tienda=9),
    Empleado(id=19, nombre="Natalia", apellidos="Iglesias Martín", telefono=3512020202, correo="natalia.iglesias@empresa.com", num_cuenta="ES1200100000020202020202", id_tienda=10),
    Empleado(id=20, nombre="Tomás", apellidos="Vidal Soto", telefono=3512121212, correo="tomas.vidal@empresa.com", num_cuenta="ES1200100000021212121212", id_tienda=10),
]

def buscar_empleado_id(id_empleado: int):
    empleados = [i for i in empleados_list if i.id == id_empleado]
    if len(empleados) != 0:
        return  empleados[0]
    else:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    
def next_id():
    return max(empleados_list, key = lambda empleado: empleado.id).id + 1

@router.get("/")
def get_empleados():
    return empleados_list

@router.get("/{id_empleado}")
def get_empleado_id(id_empleado: int):
    return buscar_empleado_id(id_empleado)

@router.post("/", status_code=201,response_model=Empleado)
def post_empleado(empleado: Empleado):
    empleado.id = next_id()
    empleados_list.append(empleado)
    return empleado

@router.put("/{id_empleado}", response_model=Empleado)
def put_empleado(id_empleado: int, empleado: Empleado):
    for index, i in enumerate(empleados_list):
        if i.id == id_empleado:
            empleado.id = id
            empleados_list[index] = empleado
            return empleado
    raise HTTPException(status_code=404, detail="Empleado not found")

@router.delete("/{id_empleado}")
def delete_empleado(id_empleado: int):
    for i in empleados_list:
        if i.id == id_empleado:
            empleados_list.remove(i)
            return {}
    raise HTTPException(status_code=404, detail="Empleado not found")

