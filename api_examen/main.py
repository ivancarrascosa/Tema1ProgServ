from fastapi import FastAPI

from routers import alumnos, colegios


app = FastAPI()

app.include_router(alumnos.router)
app.include_router(colegios.router)

@app.get("/")
def inicio():
    return {"hello": "world"}