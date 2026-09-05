from sqlalchemy import Boolean, Column
from app.config.database import Base

# Define a simple User model
class Test(Base):
    __tablename__ = "testing"
    test = Column(Boolean, primary_key=True, index=True)