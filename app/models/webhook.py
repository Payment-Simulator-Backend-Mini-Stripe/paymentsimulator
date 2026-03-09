from datetime import datetime
from app.db.session import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class WebhookConfig(Base):
    __tablename__ = "webhook_configs"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    secret = Column(String)
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    
class WebhookLog(Base):
    __tablename__ = "webhook_logs"
    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payments.id"))
    url = Column(String)
    payload = Column(String)
    status_code = Column(Integer)
    success = Column(Integer)
    attempt = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)