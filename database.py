import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

if os.getenv("GITHUB_ACTIONS") is None:
    load_dotenv(".env.local")

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}/{database}"

# Log para verificar a URL de conexão
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