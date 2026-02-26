from app.db.session import Base
from sqlalchemy import Column, Integer, String, DateTime

class Merchant(Base):
    __tablename__ = "merchants"
    id = Column(Integer, primary_key=True)
    name_store = Column(String)
    address = Column(String)
    phone = Column(String)
    registered_at = Column(DateTime)
    secret_key = Column(String)
    status = Column(String)