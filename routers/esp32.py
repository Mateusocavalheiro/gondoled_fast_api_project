from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from datetime import datetime # <- Importação necessária para o relógio
import models, schemas, database

router = APIRouter(prefix="/esp32", tags=["ESP32"])

# --- CONFIGURAÇÃO DA API KEY ---
CHAVE_SECRETA = "senha_2026!"
NOME_DO_CABECALHO = "X-API-Key"

api_key_header = APIKeyHeader(name=NOME_DO_CABECALHO, auto_error=False)

def verificar_api_key(api_key: str = Security(api_key_header)):
    if api_key == CHAVE_SECRETA:
        return api_key
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, 
        detail="Acesso Negado: API Key inválida ou ausente"
    )

# --- ROTAS PROTEGIDAS ---

@router.get("/verificar/{mac}", response_model=schemas.EtiquetaResponse)
def verificar(mac: str, db: Session = Depends(database.get_db), api_key: str = Depends(verificar_api_key)):
    db_etiqueta = db.query(models.Etiqueta).filter(models.Etiqueta.mac == mac).first()
    
    if not db_etiqueta:
        raise HTTPException(status_code=404, detail="Não cadastrada")
    
    # --- NOVO: ATUALIZAÇÃO DO HEARTBEAT ---
    db_etiqueta.ultima_visto = datetime.now()
    db_etiqueta.status = "online"
    db.commit() # Salva a nova data/hora no banco antes de responder ao ESP32
    # --------------------------------------

    return db_etiqueta

@router.post("/registrar")
def registrar(etiqueta: schemas.EtiquetaCreate, db: Session = Depends(database.get_db), api_key: str = Depends(verificar_api_key)):
    # Nota: Em versões mais recentes do Pydantic (V2), o .dict() foi substituído por .model_dump()
    # Mas se você estiver usando a V1, .dict() funciona perfeitamente.
    db_etiqueta = models.Etiqueta(**etiqueta.dict())
    db.add(db_etiqueta)
    db.commit()
    return {"status": "sucesso"}