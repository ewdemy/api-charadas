from fastapi import FastAPI, Depends
from fastapi_pagination import Page, paginate
from Utils import Params
import db
from models import Charada
from fastapi.openapi.utils import get_openapi

app = FastAPI()

@app.get("/charadas", response_model=Page[db.Charada])
async def buscar_todas_charadas(params: Params = Depends()):
    return paginate(db.busrcarTodos(), params)

@app.get("/charadas/charada-aleatoria")
async def buscar_charada_aleatoria():
    return db.buscarCharadaAleatoria()

@app.get("/charadas/{id}")
async def buscar_por_id(id: int):
    return db.buscar_por_id(id)

@app.post("/charadas", status_code = 201)
async def salvar_charada(charada: Charada):
    return db.salvar_charada(charada)

@app.put("/charadas/{id}", status_code = 200)
async def atualizar_charada(charada: Charada, id: int):
    return db.atualizar_charada(charada, id)



