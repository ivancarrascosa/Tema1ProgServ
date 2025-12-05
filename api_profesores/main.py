from fastapi.staticfiles import StaticFiles
from routers import profesores_db
from routers import auth_users
from routers import asignaturas 
from routers import profesores
from fastapi import FastAPI

app = FastAPI()

#routers
app.include_router(asignaturas.router)
app.include_router(profesores.router)
app.include_router(auth_users.router)
app.include_router(profesores_db.router)
app.mount("/static", StaticFiles(directory="static"),name="static")

@app.get("/")
def inicio():
    return {"hello": "world"}
