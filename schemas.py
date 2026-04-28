from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EtiquetaBase(BaseModel):
    nome_produto: str
    preco: float
    preco_clube: float
    prazo_validade: str

class EtiquetaCreate(EtiquetaBase):
    mac: str

class EtiquetaResponse(EtiquetaBase):
    mac: str
    status: str
    ultima_visto: datetime

    class Config:
        orm_mode = True