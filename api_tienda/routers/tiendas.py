from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(prefix="/tiendas", tags=["tiendas"])

class Tienda(BaseModel):
    id: int
    domicilio: str
    telefono: int
    precio_alquiler: float

tiendas_list = [
    Tienda(id=1, domicilio="Av. Siempre Viva 742", telefono=3511234567, precio_alquiler=1200.50),
    Tienda(id=2, domicilio="Calle Falsa 123", telefono=3519876543, precio_alquiler=950.00),
    Tienda(id=3, domicilio="Boulevard Central 456", telefono=3511112233, precio_alquiler=1500.75),
    Tienda(id=4, domicilio="San Martín 789", telefono=3512223344, precio_alquiler=800.00),
    Tienda(id=5, domicilio="Belgrano 321", telefono=3513334455, precio_alquiler=1100.25),
    Tienda(id=6, domicilio="Rivadavia 654", telefono=3514445566, precio_alquiler=1300.00),
    Tienda(id=7, domicilio="Mitre 987", telefono=3515556677, precio_alquiler=1400.00),
    Tienda(id=8, domicilio="Urquiza 159", telefono=3516667788, precio_alquiler=1250.00),
    Tienda(id=9, domicilio="Sarmiento 753", telefono=3517778899, precio_alquiler=1050.50),
    Tienda(id=10, domicilio="Lavalle 852", telefono=3518889900, precio_alquiler=990.00),
]

def buscar_tienda_id(id_tienda: int):
    tiendas = [i for i in tiendas_list if i.id == id_tienda]
    if len(tiendas) != 0:
        return  tiendas[0]
    else:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    
def next_id():
    return max(tiendas_list, key = lambda tienda: tienda.id).id + 1

@router.get("/")
def getTiendas():
    return tiendas_list

@router.get("/{idTienda}")
def getTiendaId(idTienda: int):
    return buscar_tienda_id(idTienda)

@router.post("/", status_code=201, response_model=Tienda)
def post_tienda(tienda: Tienda):
    tienda.id = next_id()
    tiendas_list.append(tienda)
    return tienda

@router.put("/{id}", response_model=Tienda)
def put_tienda(id: int, tienda: Tienda):
    for index, saved_tienda in enumerate(tiendas_list):
        if (saved_tienda.id == id):
            tienda.id = saved_tienda.id
            tiendas_list[index] = tienda
            return tienda
    raise HTTPException(status_code=404, detail="Tienda not found")

@router.delete("/{id}")
def delete_tienda(id: int):
    for tienda in tiendas_list:
        if tienda.id == id:
            tiendas_list.remove(tienda)
            return {}
    raise HTTPException(status_code=404, detail="Tienda not found")