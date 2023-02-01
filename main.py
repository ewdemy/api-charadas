from fastapi import FastAPI, Depends, Response, status
from fastapi_pagination import Page, paginate
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from Utils import Params
import repository
from models import Charada
import os
import bcrypt

SECRET = os.urandom(24).hex()

app = FastAPI()

manager = LoginManager(SECRET, token_url='/charadas/auth/login')

@manager.user_loader()
def load_user(email: str):
    user = repository.buscar_usuario_por_email(email)
    return user


@app.post('/charadas/auth/login')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)

    if user is None or not valida_senha(password, user.password.encode()):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get("/charadas", response_model=Page[repository.Charada])
async def buscar_todas_charadas(params: Params = Depends(), user=Depends(manager)):
    return paginate(repository.buscar_todos(), params)


@app.get("/charadas/charada-aleatoria")
async def buscar_charada_aleatoria():
    return repository.buscar_charada_aleatoria()


@app.get("/charadas/{id}")
async def buscar_por_id(id: int, user=Depends(manager)):
    return repository.buscar_por_id(id)


@app.post("/charadas", status_code=201)
async def salvar_charada(charada: Charada, user=Depends(manager)):
    return repository.salvar_charada(charada)


@app.put("/charadas/{id}", status_code=200)
async def atualizar_charada(charada: Charada, id: int, user=Depends(manager)):
    return repository.atualizar_charada(charada, id)


@app.delete("/charadas/{id}", status_code=204)
async def deletar_charada(id: int, user=Depends(manager)):
    repository.deletar_charada(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def valida_senha(senha_digitada, senha_hash):
    return bcrypt.hashpw(senha_digitada.encode(), senha_hash) == senha_hash
