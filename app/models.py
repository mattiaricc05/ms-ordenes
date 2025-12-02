from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base

class Retiro(Base):
    __tablename__ = "retiros_ordenes"
    
    id = Column(Integer, primary_key=True, index=True)
    producto = Column(String(200), nullable=False)
    cantidad = Column(Integer, nullable=False)
    operario = Column(String(100), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())