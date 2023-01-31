from fastapi import FastAPI, Depends, Response, status
from fastapi_pagination import Page, paginate
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from Utils import Params
import repository
from models import Charada

SECRET = 'your-secret-key'

app = FastAPI()

manager = LoginManager(SECRET, token_url='/charadas/auth/login')
fake_db = {'johndoe@e.mail': {'password': 'hunter2'}}

@manager.user_loader()
def load_user(email: str):  # could also be an asynchronous function
    user = fake_db.get(email)
    return user

@app.post('/charadas/auth/login')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.get("/charadas", response_model=Page[repository.Charada])
async def buscar_todas_charadas(params: Params = Depends(), user=Depends(manager)):
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

@app.delete("/charadas/{id}", status_code = 204)
async def deletar_charada(id: int):
    repository.deletar_charada(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



