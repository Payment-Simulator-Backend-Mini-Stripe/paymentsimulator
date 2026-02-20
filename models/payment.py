from db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    status = Column(String)
    created_on= Column(DateTime)
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    
