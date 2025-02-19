from fastapi import FastAPI
from fastapi.params import Body
from fastapi import Depends
from fastapi import status
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from model import Base
from database import engine
from scraping import scraping_ufu
import model
from fastapi.middleware.cors import CORSMiddleware
import classes

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    'http://localhost:3000'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get("/")
def read_root():
    return {"Hello": "lala"}

@app.post("/criar", status_code=status.HTTP_201_CREATED)
def criar_valores(nova_mensagem: classes.Mensagem, db: Session = Depends(get_db)):
    mensagem_criada = model.Model_Mensagem(titulo=nova_mensagem.titulo,
    conteudo=nova_mensagem.conteudo, publicada=nova_mensagem.publicada)
    mensagem_criada = model.Model_Mensagem(**nova_mensagem.model_dump())
    db.add(mensagem_criada)
    db.commit()    
    db.refresh(mensagem_criada)
    return {"Mensagem": mensagem_criada}

@app.get("/quadrado/{num}")
def square(num: int):
    return num ** 2

@app.get("/mensagens", response_model=List[classes.Mensagem], status_code=status.HTTP_200_OK)
async def buscar_valores(db: Session = Depends(get_db), skip: int = 0, limit: int=100):
    mensagens = db.query(model.Model_Mensagem).offset(skip).limit(limit).all()
    return mensagens

@app.get("/scraping", status_code=status.HTTP_201_CREATED)
def executar_scrape(db: Session = Depends(get_db)):
    return scraping_ufu(db)