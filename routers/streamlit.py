from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["Admin Streamlit"])

@router.get("/etiquetas")
def listar_todas(db: Session = Depends(database.get_db)):
    return db.query(models.Etiqueta).all()

@router.patch("/atualizar/{mac}")
def atualizar_etiqueta(mac: str, novos_dados: schemas.EtiquetaBase, db: Session = Depends(database.get_db)):
    db_etiqueta = db.query(models.Etiqueta).filter(models.Etiqueta.mac == mac).first()
    
    if not db_etiqueta:
        raise HTTPException(status_code=404, detail="Etiqueta não encontrada")

    # Guardar os dados antigos para o log
    payload_anterior = {
        "nome": db_etiqueta.nome_produto,
        "preco": db_etiqueta.preco,
        "preco_clube": db_etiqueta.preco_clube,
        "validade": db_etiqueta.prazo_validade
    }

    # Atualizar os campos
    db_etiqueta.nome_produto = novos_dados.nome_produto
    db_etiqueta.preco = novos_dados.preco
    db_etiqueta.preco_clube = novos_dados.preco_clube
    db_etiqueta.prazo_validade = novos_dados.prazo_validade

    # Gerar o LOG
    novo_log = models.LogEtiqueta(
        mac_etiqueta=mac,
        payload_anterior=payload_anterior,
        payload_novo=novos_dados.dict()
    )

    db.add(novo_log)
    db.commit()
    return {"status": "atualizado", "log_id": novo_log.id}

@router.get("/logs/{mac}")
def ver_logs(mac: str, db: Session = Depends(database.get_db)):
    return db.query(models.LogEtiqueta).filter(models.LogEtiqueta.mac_etiqueta == mac).order_by(models.LogEtiqueta.data_alteracao.desc()).all()