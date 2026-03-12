from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    phone = Column(String, unique=True)

    email = Column(String, unique=True)

    name = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)