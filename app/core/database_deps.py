from sqlalchemy.orm import Session
from app.core import db_postgresql as database

def get_db_session():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()