import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

if os.getenv("GITHUB_ACTIONS") is None:
    load_dotenv(".env.local")

user = "postgres"
password = "123"
database = "prototipo"
host = "postgres"

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}/{database}"

print(f"Database URL: {SQLALCHEMY_DATABASE_URL}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
try:
    with engine.connect() as conn:
        print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Erro ao conectar ao banco: {e}")