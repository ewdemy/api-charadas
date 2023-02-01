import sqlite3
from fastapi import HTTPException
from models import Charada, Usuario

db = sqlite3.connect("database.sqlite", check_same_thread=False)

cursor = db.cursor()

def buscar_todos():
    charadas = []
    cursor.execute("select id, pergunta, resposta from charadas")
    data = cursor.fetchall()

    for i in data:
        charadas.append(to_charada(i))

    return charadas

def buscar_charada_aleatoria():
    cursor.execute("select id, pergunta, resposta from charadas order by random() limit 1")
    charada = cursor.fetchone()
    return to_charada(charada)

def buscar_por_id(id):
    cursor.execute(f"select id, pergunta, resposta from charadas where id = {id}")
    charada = cursor.fetchone()
    if charada is None:
        raise HTTPException(status_code=404, detail=f"Charada com id: {id} não existe!")
    return to_charada(charada)

def salvar_charada(charada: Charada):
    cursor.execute("insert into charadas(pergunta, resposta, createdAt, updatedAt) values ('"+charada.pergunta+"', '"+charada.resposta+"', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)")
    db.commit()
    cursor.execute(f"select id, pergunta, resposta from charadas where id = (SELECT MAX( id ) from charadas)")
    charada = cursor.fetchone()
    return to_charada(charada)

def atualizar_charada(charada: Charada, id: int):
    cursor.execute(f"update charadas set pergunta = '"+charada.pergunta+"', resposta = '"+charada.resposta+"', updatedAt = CURRENT_TIMESTAMP where id = '"+str(id)+"'")
    db.commit()
    cursor.execute(f"select id, pergunta, resposta from charadas where id = '"+str(id)+"'")
    charada = cursor.fetchone()
    return to_charada(charada)

def deletar_charada(id: int):
    buscar_por_id(id)
    cursor.execute(f"delete from charadas where id = '"+str(id)+"'")
    db.commit()

def buscar_usuario_por_email(email):
    cursor.execute(f"select id, nome, email, password from usuarios where email = '"+str(email)+"'")
    usuario = cursor.fetchone()
    if usuario is None:
        return usuario
    return to_usuario(usuario)

def to_charada(tupla):
    charada = Charada(id=tupla[0], pergunta=tupla[1], resposta=tupla[2])
    return charada

def to_usuario(tupla):
    usuario = Usuario(id=tupla[0], nome=tupla[1], email=tupla[2], password=tupla[3])
    return usuario


