from fastapi import FastAPI, Depends
from fastapi_pagination import Page, paginate
from Utils import Params
import repository
from models import Charada

app = FastAPI()

@app.get("/charadas", response_model=Page[repository.Charada])
async def buscar_todas_charadas(params: Params = Depends()):
    return paginate(repository.busrcarTodos(), params)

@app.get("/charadas/charada-aleatoria")
async def buscar_charada_aleatoria():
    return repository.buscarCharadaAleatoria()

@app.get("/charadas/{id}")
async def buscar_por_id(id: int):
    return repository.buscar_por_id(id)

@app.post("/charadas", status_code = 201)
async def salvar_charada(charada: Charada):
    return repository.salvar_charada(charada)

@app.put("/charadas/{id}", status_code = 200)
async def atualizar_charada(charada: Charada, id: int):
    return repository.atualizar_charada(charada, id)



