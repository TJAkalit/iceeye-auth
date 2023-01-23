from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    DateTime,
    func,
)

Base = declarative_base()

class User(Base):
    
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    login = Column(String(64))
    password = Column(String(60))
    email = Column(String(128))
    first_name = Column(String(32))
    last_name = Column(String(32))
    middle_name = Column(String(32))
    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, onupdate=func.now())