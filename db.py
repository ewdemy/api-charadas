import sqlite3
from fastapi import HTTPException
from models import Charada

db = sqlite3.connect("database.sqlite")

cursor = db.cursor()

def busrcarTodos():
    charadas = []
    cursor.execute("select id, pergunta, resposta from charadas")
    data = cursor.fetchall()

    for i in data:
        charadas.append(toCharada(i))

    return charadas

def buscarCharadaAleatoria():
    cursor.execute("select id, pergunta, resposta from charadas order by random() limit 1")
    charada = cursor.fetchone()
    return toCharada(charada)

def buscar_por_id(id):
    cursor.execute(f"select id, pergunta, resposta from charadas where id = {id}")
    charada = cursor.fetchone()
    if charada is None:
        raise HTTPException(status_code=404, detail=f"Charada com id: {id} não existe!")
    return toCharada(charada)

def salvar_charada(charada: Charada):
    cursor.execute("insert into charadas(pergunta, resposta, createdAt, updatedAt) values ('"+charada.pergunta+"', '"+charada.resposta+"', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)")
    commit = db.commit()
    print(commit)
    cursor.execute(f"select id, pergunta, resposta from charadas where id = (SELECT MAX( id ) from charadas)")
    charada = cursor.fetchone()
    return toCharada(charada)


def toCharada(tupla):
    charada = Charada(id=tupla[0], pergunta=tupla[1], resposta=tupla[2])
    return charada


