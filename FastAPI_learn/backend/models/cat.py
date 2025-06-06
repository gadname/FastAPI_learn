from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql.functions import current_timestamp
from db.base_class import Base

class Cat(Base):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    breed = Column(String(50))
    age = Column(Integer)
    weight = Column(Float)
    created_at = Column(DateTime, server_default=current_timestamp())
    updated_at = Column(DateTime, server_default=current_timestamp(), onupdate=current_timestamp())