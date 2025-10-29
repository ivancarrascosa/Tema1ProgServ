from fastapi import FastAPI
from routers import empleados, tiendas

app = FastAPI()

app.include_router(empleados.router)
app.include_router(tiendas.router)

@app.get("/")
def get():
    return {"Hello": "world"}