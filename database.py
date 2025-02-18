import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Carregar variáveis de ambiente locais
if os.getenv("GITHUB_ACTIONS") is None:
    load_dotenv(".env.local")

# Definir valores padrão para evitar `None`
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "123")
database = os.getenv("POSTGRES_DB", "prototipo")
host = os.getenv("POSTGRES_HOST", "localhost")  # Padrão correto

# Criar DATABASE_URL a partir das variáveis ou do Secret
DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{user}:{password}@{host}:5432/{database}")

if DATABASE_URL is None or "None" in DATABASE_URL:
    raise ValueError("Erro: DATABASE_URL não está definida corretamente!")

# Criar engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
