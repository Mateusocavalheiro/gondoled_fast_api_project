from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
import models, schemas, database

router = APIRouter(prefix="/esp32", tags=["ESP32"])

# --- CONFIGURAÇÃO DA API KEY ---
CHAVE_SECRETA = "senha_2026!" # Invente a sua chave aqui
NOME_DO_CABECALHO = "X-API-Key"

# Define que a chave deve vir no cabeçalho da requisição HTTP
api_key_header = APIKeyHeader(name=NOME_DO_CABECALHO, auto_error=False)

# Função "Cadeado": Verifica se a chave recebida é igual à secreta
def verificar_api_key(api_key: str = Security(api_key_header)):
    if api_key == CHAVE_SECRETA:
        return api_key
    
    # Se a chave estiver errada ou não for enviada, bloqueia com Erro 403 (Proibido)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, 
        detail="Acesso Negado: API Key inválida ou ausente"
    )

# --- ROTAS PROTEGIDAS ---
# Repare no: Depends(verificar_api_key) - Ele obriga a passar pelo cadeado primeiro

@router.get("/verificar/{mac}", response_model=schemas.EtiquetaResponse)
def verificar(mac: str, db: Session = Depends(database.get_db), api_key: str = Depends(verificar_api_key)):
    db_etiqueta = db.query(models.Etiqueta).filter(models.Etiqueta.mac == mac).first()
    if not db_etiqueta:
        raise HTTPException(status_code=404, detail="Não cadastrada")
    return db_etiqueta

@router.post("/registrar")
def registrar(etiqueta: schemas.EtiquetaCreate, db: Session = Depends(database.get_db), api_key: str = Depends(verificar_api_key)):
    db_etiqueta = models.Etiqueta(**etiqueta.dict())
    db.add(db_etiqueta)
    db.commit()
    return {"status": "sucesso"}