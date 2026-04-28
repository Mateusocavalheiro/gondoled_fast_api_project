from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey, JSON
from datetime import datetime
from database import Base

class Etiqueta(Base):
    __tablename__ = "etiquetas"
    mac = Column(String(50), primary_key=True, index=True)
    nome_produto = Column(String(255))                     
    preco = Column(Float)
    preco_clube = Column(Float)
    prazo_validade = Column(String(50))
    status = Column(String(50), default="online")
    ultima_visto = Column(DateTime, default=datetime.utcnow)

class LogEtiqueta(Base):
    __tablename__ = "logs_etiquetas"
    id = Column(Integer, primary_key=True, index=True)
    mac_etiqueta = Column(String(50), ForeignKey("etiquetas.mac"))
    payload_anterior = Column(JSON)
    payload_novo = Column(JSON)
    data_alteracao = Column(DateTime, default=datetime.utcnow)