def profesor_schema(profesor) -> dict:
    #El id en la base de datos es _id
    return {
        "id": str(profesor["_id"]),
        "DNI": str(profesor["DNI"]),
        "nombre": str(profesor["nombre"]),
        "apellidos": str(profesor["apellidos"]),
        "telefono": str(profesor["telefono"]),
        "direccion": str(profesor["direccion"]),
        "cuentaBancaria": str(profesor["cuentaBancaria"])
    }

def profesores_schema(profesores) -> list:
    return [profesor_schema(profesor) for profesor in profesores]
