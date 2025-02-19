from pydantic import BaseModel

class Mensagem(BaseModel):
    titulo: str
    conteudo: str
    publicada: bool = True

class MenuNav(BaseModel):
    menuNav: str
    link: str