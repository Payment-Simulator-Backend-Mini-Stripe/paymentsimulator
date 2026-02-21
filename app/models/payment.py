from app.db.session import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    status = Column(String)
    created_at= Column(DateTime)
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    
