from datetime import datetime

from pydantic import BaseModel

class Charada(BaseModel):
    id: int = None
    pergunta: str
    resposta: str

    class Config:
        orm_mode = True
