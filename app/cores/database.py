# app/infrastructure/database.py
from sqlmodel import Session, create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False)


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
