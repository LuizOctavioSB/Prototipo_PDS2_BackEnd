from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
import classes
import model
from database import engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Mensagem(BaseModel):
    titulo: str
    conteudo: str
    publicada: bool = True

@app.get("/")
def read_root():
    return {"Hello": "lala"}

@app.get("/quadrado/{num}")
def square(num: int):
    return num ** 2

@app.post("/criar")
def criar_valores(nova_mensagem: Mensagem):
    print(nova_mensagem)
    return {"Mensagem": f"Título: {nova_mensagem.titulo} Conteúdo: {nova_mensagem.conteudo} Publicada: {nova_mensagem.publicada}"}
