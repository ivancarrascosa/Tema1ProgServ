from fastapi.staticfiles import StaticFiles
from routers import asignaturas 
from routers import profesores
from fastapi import FastAPI

app = FastAPI()

#routers
app.include_router(asignaturas.router)
app.include_router(profesores.router)
app.mount("/static", StaticFiles(directory="static"),name="static")

@app.get("/")
def inicio():
    return {"hello": "world"}
