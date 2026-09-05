from sqlalchemy import select, Column, Integer, String
from app.config.database import Base, engine, get_db

# Define a simple User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(100))