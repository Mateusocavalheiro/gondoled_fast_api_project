from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import models, schemas, database, os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(prefix="/admin", tags=["Streamlit / Admin"])

# Convertendo para inteiro, pois o .env sempre retorna texto (string)
MINUTOS_OFFLINE = int(os.getenv("TEMPO_OFFLINE_MINUTOS", 7))

@router.get("/etiquetas", response_model=List[schemas.EtiquetaResponse])
def listar_etiquetas(db: Session = Depends(database.get_db)):
    etiquetas = db.query(models.Etiqueta).all()
    agora = datetime.now()
    limite = timedelta(minutes=MINUTOS_OFFLINE) # 5 min do ESP32 + 2 min de margem

    for e in etiquetas:
        # Lógica de Heartbeat: se não enviou sinal recentemente, marca como offline
        if (agora - e.ultima_visto) > limite:
            e.status = "offline"
    
    db.commit()
    return etiquetas

@router.patch("/atualizar/{mac}", response_model=schemas.EtiquetaResponse)
def atualizar_etiqueta(mac: str, dados_novos: schemas.EtiquetaBase, db: Session = Depends(database.get_db)):
    db_etiqueta = db.query(models.Etiqueta).filter(models.Etiqueta.mac == mac).first()
    
    if not db_etiqueta:
        raise HTTPException(status_code=404, detail="Etiqueta não encontrada")

    # --- LÓGICA DE LOG ---
    # Guardamos o estado antigo antes de atualizar
    payload_anterior = {
        "nome_produto": db_etiqueta.nome_produto,
        "preco": db_etiqueta.preco,
        "preco_clube": db_etiqueta.preco_clube,
        "prazo_validade": db_etiqueta.prazo_validade
    }

    # Atualizamos os campos
    for key, value in dados_novos.dict().items():
        setattr(db_etiqueta, key, value)

    # Criamos o registro de log
    novo_log = models.LogEtiqueta(
        mac_etiqueta=mac,
        payload_anterior=payload_anterior,
        payload_novo=dados_novos.dict(),
        data_alteracao=datetime.now()
    )

    db.add(novo_log)
    db.commit()
    db.refresh(db_etiqueta)
    
    return db_etiqueta

@router.get("/logs/{mac}", response_model=List[schemas.LogResponse])
def obter_historico(mac: str, db: Session = Depends(database.get_db)):
    logs = db.query(models.LogEtiqueta).filter(models.LogEtiqueta.mac_etiqueta == mac).order_by(models.LogEtiqueta.data_alteracao.desc()).all()
    return logs