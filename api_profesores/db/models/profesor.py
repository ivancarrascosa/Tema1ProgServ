from typing import Optional
from pydantic import BaseModel

class Profesor(BaseModel):
    id: Optional [str] = None
    DNI: str
    nombre: str
    apellidos: str
    telefono: str
    direccion: str
    cuentaBancaria: str