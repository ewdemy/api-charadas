from datetime import datetime

from pydantic import BaseModel

class Charada(BaseModel):
    id: int = None
    pergunta: str
    resposta: str

    class Config:
        orm_mode = True

class Usuario(BaseModel):
    id: int = None
    nome: str
    email: str
    password: str

    class Config:
        orm_mode = True
