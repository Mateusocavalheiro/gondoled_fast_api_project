from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/esp32", tags=["ESP32"])

@router.get("/verificar/{mac}", response_model=schemas.EtiquetaResponse)
def verificar(mac: str, db: Session = Depends(database.get_db)):
    db_etiqueta = db.query(models.Etiqueta).filter(models.Etiqueta.mac == mac).first()
    if not db_etiqueta:
        raise HTTPException(status_code=404, detail="Não cadastrada")
    return db_etiqueta

@router.post("/registrar")
def registrar(etiqueta: schemas.EtiquetaCreate, db: Session = Depends(database.get_db)):
    db_etiqueta = models.Etiqueta(**etiqueta.dict())
    db.add(db_etiqueta)
    db.commit()
    return {"status": "sucesso"}