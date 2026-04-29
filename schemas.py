from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any

# Esquema base com os campos que você definiu
class EtiquetaBase(BaseModel):
    nome_produto: str
    preco: float
    preco_clube: float
    prazo_validade: str

# Para o ESP32 criar o registro inicial
class EtiquetaCreate(EtiquetaBase):
    mac: str

# Resposta padrão para o hardware e Streamlit
class EtiquetaResponse(EtiquetaBase):
    mac: str
    status: str
    ultima_visto: datetime

    class Config:
        from_attributes = True

# Esquema para os Logs
class LogResponse(BaseModel):
    id: int
    mac_etiqueta: str
    payload_anterior: Any
    payload_novo: Any
    data_alteracao: datetime

    class Config:
        from_attributes = True